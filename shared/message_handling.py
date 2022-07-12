"""
.. module:: message_handling
   :platform: Unix
   :synopsis: A module that processes V2GTP messages.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from shared.messages import V2GTPMessage
from shared.global_values import PROTOCOL_VERSION
from shared.log import logger
import lxml
from shared.global_values import SDP_PAYLOAD_TYPES, MAX_PAYLOAD_LENGTH, APP_PROTOCOL_EXIG, COMMON_MESSAGES_EXIG, \
    DC_MESSAGES_EXIG, APP_PROTOCOL_XSD, COMMON_MESSAGES_XSD, DC_MESSAGES_XSD

import jpype
import os
import jpype.imports
from jpype.types import *

# The code below allows usage of Java classes by starting a JVM inside Python. This way, we can access variables
# initialized in the VM and use functions written in Java.
classpath = f'{str.join(":", ["../shared/lib/" + name for name in os.listdir("../shared/lib/")])}'
jpype.startJVM(jpype.getDefaultJVMPath(), '-ea', "-Djava.class.path=%s" % classpath)
from java.io import FileInputStream, InputStream, ByteArrayInputStream, ByteArrayOutputStream, StringWriter, FileWriter
from java.lang import String
from org.openexi.scomp import EXISchemaReader
from org.openexi.schema import EXISchema
from org.openexi.sax import Transmogrifier, EXIReader
from org.openexi.proc.grammars import GrammarCache
from org.openexi.proc.common import AlignmentType, GrammarOptions
from org.xml.sax import InputSource
from java.nio.charset import Charset
from javax.xml.transform.sax import SAXTransformerFactory
from javax.xml.transform.stream import StreamResult
from javax.xml.parsers import SAXParserFactory


class Singleton(type):
    """This is a singleton design pattern class.

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def open_exi_schema(filepath: str) -> EXISchema:
    """Loads EXISchema. Relies on Java classes.

    :param filepath: The path to the EXIG file.
    :return: EXISchema -- the object containing the schema.
    """
    schema_reader = EXISchemaReader()
    schema = None
    fis = None
    try:
        fis = FileInputStream(filepath)
        schema = schema_reader.parse(fis)
    finally:
        if fis:
            fis.close()
        return schema


class MessageHandler(metaclass=Singleton):
    """This is the class that will process every single V2GTP message.

    """
    transmogrifier = Transmogrifier()
    transmogrifier.setAlignmentType(AlignmentType.bitPacked)
    options = GrammarOptions.DEFAULT_OPTIONS
    transmogrifier.setBlockSize(1000000)
    transmogrifier.setValueMaxLength(-1)
    transmogrifier.setValuePartitionCapacity(0)

    sax_transformer_factory = JObject(SAXTransformerFactory.newInstance(), SAXTransformerFactory)
    sax_parser_factory = SAXParserFactory.newInstance()
    sax_parser_factory.setNamespaceAware(True)
    transformer_handler = sax_transformer_factory.newTransformerHandler()
    reader = EXIReader()
    reader.setAlignmentType(AlignmentType.bitPacked)
    reader.setBlockSize(1000000)
    reader.setValueMaxLength(-1)
    reader.setValuePartitionCapacity(0)
    reader.setContentHandler(transformer_handler)

    ap_schema = open_exi_schema(APP_PROTOCOL_EXIG)
    ap_grammar_cache = GrammarCache(ap_schema, options)

    common_schema = open_exi_schema(COMMON_MESSAGES_EXIG)
    common_grammar_cache = GrammarCache(common_schema, options)

    dc_schema = open_exi_schema(DC_MESSAGES_EXIG)
    dc_grammar_cache = GrammarCache(dc_schema, options)

    def __init__(self):
        self.xml_SAP_validator = lxml.etree.XMLSchema(file=APP_PROTOCOL_XSD)
        self.xml_Common_validator = lxml.etree.XMLSchema(file=COMMON_MESSAGES_XSD)
        self.xml_DC_validator = lxml.etree.XMLSchema(file=DC_MESSAGES_XSD)

    def is_valid(self, v2gtp_message: V2GTPMessage) -> bool:
        if self.is_version_valid(v2gtp_message) and self.is_version_valid(v2gtp_message) and \
                self.is_payload_type_correct(v2gtp_message) and self.is_payload_length_correct(v2gtp_message):
            logger.info("Message is valid.")
            return True
        logger.warn("Message is not valid.")
        return False

    @staticmethod
    def is_version_valid(v2gtp_message: V2GTPMessage) -> bool:
        protocol_version = v2gtp_message.get_protocol_version()
        if protocol_version != PROTOCOL_VERSION:
            logger.error("Protocol version mismatch.")
            return False
        if v2gtp_message.get_inverse_protocol_version() != protocol_version ^ 0xff:
            logger.error("Inverse protocol version mismatch.")
            return False
        return True

    @staticmethod
    def is_payload_type_correct(v2gtp_message: V2GTPMessage) -> bool:
        payload_type = v2gtp_message.get_payload_type()
        for key in SDP_PAYLOAD_TYPES.keys():
            if payload_type == key:
                return True
        logger.error("Unrecognized payload type.")
        return False

    @staticmethod
    def is_payload_length_correct(v2gtp_message: V2GTPMessage) -> bool:
        payload_length = v2gtp_message.get_payload_length()
        if 0 < payload_length < MAX_PAYLOAD_LENGTH:
            return True
        logger.error("Wrong payload size.")
        return False

    # @staticmethod
    # def open_exi_schema(filepath: str) -> EXISchema:
    #     """Loads EXISchema. Relies on Java classes.
    #
    #     :param filepath: The path to the EXIG file.
    #     :return: EXISchema -- the object containing the schema.
    #     """
    #     schema_reader = EXISchemaReader()
    #     schema = None
    #     fis = None
    #     try:
    #         fis = FileInputStream(filepath)
    #         schema = schema_reader.parse(fis)
    #     finally:
    #         if fis:
    #             fis.close()
    #         return schema

    @staticmethod
    def encode(xml_contents: str, type_msg: str) -> str:
        """Turns a human-readable string to an EXI-encoded string. Relies on Java classes.

        :param xml_contents: The XML string to be encoded.
        :param type_msg: The type of message used.
        :return: str -- the encoded result.
        """
        contents = String(xml_contents)
        input = None
        output = None
        try:
            t = MessageHandler.transmogrifier
            input = ByteArrayInputStream(contents.getBytes(Charset.forName("ASCII")));
            output = ByteArrayOutputStream();
            if type_msg == "SAP":
                t.setGrammarCache(MessageHandler.ap_grammar_cache);
            elif type_msg == "Common":
                t.setGrammarCache(MessageHandler.common_grammar_cache);
            elif type_msg == "DC":
                t.setGrammarCache(MessageHandler.dc_grammar_cache);
            else:
                raise Exception("Unknown message type")
            t.setOutputStream(output);
            t.encode(InputSource(input));
            result = output.toByteArray()
        finally:
            if input:
                input.close()
            if output:
                output.close()
            return result

    @staticmethod
    def decode(exi_contents: bytes, type_msg: str) -> str:
        """Turns encoded EXI bytes to human-readable string. Relies on Java classes.

        :param exi_contents: The EXI encoded contents.
        :param type_msg: The type of message used.
        :return: str -- the decoded string.
        """
        input = None
        output = None
        stringWriter = StringWriter()
        result = None
        try:
            input = ByteArrayInputStream(exi_contents)
            r = MessageHandler.reader
            tf_handler = MessageHandler.transformer_handler
            if type_msg == "SAP":
                r.setGrammarCache(MessageHandler.ap_grammar_cache);
            elif type_msg == "Common":
                r.setGrammarCache(MessageHandler.common_grammar_cache);
            elif type_msg == "DC":
                r.setGrammarCache(MessageHandler.dc_grammar_cache);
            else:
                raise Exception("Unknown message type")

            tf_handler.setResult(StreamResult(stringWriter))
            r.parse(InputSource(input))
            result = stringWriter.getBuffer().toString()
        finally:
            if input:
                input.close()
            if output:
                output.close()
            return str(result)

    def supported_app_to_exi(self, xml_contents) -> bytes:
        logger.info("Supported App Protocol message to be encoded")
        if self.is_xml_valid(xml_contents, 'SAP'):
            logger.info("Message is valid against Schema XSD")
            return self.encode(xml_contents, "SAP")
        else:
            raise Exception("XML is not valid against schema")

    def v2g_common_msg_to_exi(self, xml_contents) -> bytes:
        logger.info("Common message to be encoded")
        if self.is_xml_valid(xml_contents, 'Common'):
            logger.info("Message is valid against Schema XSD")
            return self.encode(xml_contents, "Common")
        else:
            raise Exception("XML is not valid against schema")

    def v2g_dc_msg_to_exi(self, xml_contents) -> bytes:
        logger.info("DC message to be encoded")
        if self.is_xml_valid(xml_contents, 'DC'):
            logger.info("Message is valid against Schema XSD")
            return self.encode(xml_contents, "DC")
        else:
            raise Exception("XML is not valid against schema")

    def exi_to_supported_app(self, exi_contents) -> str:
        logger.info("Supported App Protocol message to be decoded")
        return self.decode(exi_contents, "SAP")

    def exi_to_v2g_common_msg(self, exi_contents) -> str:
        logger.info("Common message to be decoded")
        return self.decode(exi_contents, "Common")

    def exi_to_v2g_dc_msg(self, exi_contents) -> str:
        logger.info("DC message to be decoded")
        return self.decode(exi_contents, "DC")

    @staticmethod
    def unmarshall(xml):
        """Extracts data from XML string and turns it to an object understood by the machine.

        :param xml: The XLM string to extract data from.
        :return: object -- the resulting XML object.
        """
        parser = XmlParser(context=XmlContext())
        xml_object = parser.from_string(xml)
        return xml_object

    @staticmethod
    def marshall(message) -> str:
        """Turns an XML object to a string.

        :param message: The XML object to be processed.
        :print_xml: Boolean to request printing, default True
        :return: str -- the resulting XML string.
        """
        config = SerializerConfig(pretty_print=True)
        serializer = XmlSerializer(config=config)
        xml_string = serializer.render(message)
        return xml_string

    def is_xml_valid(self, xml, msg_type):
        """This method allows to check if an XML message is valid using the corresponding XSD.

        :param xml: Input XML file
        :param msg_type: message type based on schema
        :return: boolean statement - true: valid, false: invalid
        """
        is_valid = False
        xml_file = lxml.etree.XML(xml.encode("ascii"))
        if msg_type == 'SAP':
            validator = self.xml_SAP_validator
        elif msg_type == 'Common':
            validator = self.xml_Common_validator
        elif msg_type == 'DC':
            validator = self.xml_DC_validator
        try:
            validator.assertValid(xml_file)
            is_valid = True
        except lxml.etree.DocumentInvalid as e:
            logger.warn(e)
            logger.warn(xml)
        finally:
            return is_valid
