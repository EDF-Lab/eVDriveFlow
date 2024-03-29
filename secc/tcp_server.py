"""
.. module:: tcp_server
   :platform: Unix
   :synopsis: A module that implements 15118 TCP server.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import asyncio
import ssl
from asyncio import transports
from typing import Optional

import hexdump
import transitions
from secc.evse_session import EVSESession
from shared.log import logger
from shared.global_values import SECC_CERTCHAIN, SECC_KEYFILE, PASSPHRASE, EVCC_CERTIFICATE_AUTHORITY, SECURITY_PROTOCOL
from shared.message_handling import MessageHandler
from shared.messages import V2GTPMessage, EXIMessage, SupportedAppMessage, EXIDCMessage
from shared.payloads import EXIPayload
from shared.reaction_message import PauseSession, SendMessage, TerminateSession


class TCPServerProtocol(asyncio.Protocol):
    """This is the protocol used by the SECC server to communicate with the EV.

    """
    def __init__(self, controller):
        """Basic constructor.

        :param controller: The controller that will handle the data.
        """
        self._observers = []
        self.transport = None
        self.__session = None
        self.message_handler = MessageHandler()
        self.controller = controller
        super(TCPServerProtocol, self).__init__()

    def connection_made(self, transport: transports.BaseTransport) -> None:
        logger.info("Connection made. Starting new communication session.")
        self.session = EVSESession(self.controller)
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        addr = self.transport.get_extra_info('peername')
        logger.info("Received request from %s.", addr)
        packet = EXIMessage(data)
        if packet.get_payload_type() == 0x8001:
            packet = SupportedAppMessage(data)
        if packet.get_payload_type() == 0x8004:
            packet = EXIDCMessage(data)
        self.process_incoming_message(packet)

    def eof_received(self) -> Optional[bool]:
        logger.info('Received EOF.')
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            logger.error('{}.'.format(exc))
        else:
            logger.info('Closing connection.')
        super().connection_lost(exc)

    def process_incoming_message(self, v2gtp_message: V2GTPMessage):
        """Processes incoming messages.

        :param v2gtp_message: The incoming message.
        :return:
        """
        if self.message_handler.is_valid(v2gtp_message):
            message_type = v2gtp_message.get_payload_type()
            payload = v2gtp_message.payload.getfieldval("payloadContent")

            logger.debug("Received EXI msg to be decoded: " + hexdump.dump(payload, len(payload), ' '))
            if message_type == 0x8001:
                logger.info("Payload type: 0x8001")
                xml = self.message_handler.exi_to_supported_app(payload)
            elif message_type == 0x8004:
                logger.info("Payload type: 0x8004")
                xml = self.message_handler.exi_to_v2g_dc_msg(payload)
            elif message_type == 0x8002:
                logger.info("Payload type: 0x8002")
                xml = self.message_handler.exi_to_v2g_common_msg(payload)
            else:
                raise Exception("Unknown payload type")
            logger.debug("Message successfully decoded")
            logger.debug("XML message received: " + xml)
            xml_object = self.message_handler.unmarshall(xml)
            request_type = type(xml_object).__name__ # TODO: This method takes too long
            logger.info("Received %s.", request_type)
            self.controller.data_model.state = request_type
            try:
                message_name = "Process" + request_type[:-3] + "Req"
                getattr(self.session, "to_" + message_name)()
                if self.session.sequence_timer:
                    self.session.reset_sequence_timer()
                self.session.update_timers()
                self.session.message_timer.start()
            except (transitions.core.MachineError, TypeError) as e:
                logger.warning(e)
                self.process_reaction(TerminateSession())
            reaction = self.session.get_state(self.session.state).process_payload(xml_object)
            self.process_reaction(reaction)
        else:
            self.process_reaction(TerminateSession())

    def process_reaction(self, reaction):
        """Depending on the incoming message, processes the resulting reaction.

        :param reaction: The reaction generated by the message.
        :return:
        """
        xml = self.message_handler.marshall(reaction.message)
        logger.debug("XML message to be sent: " + xml)
        logger.debug("Encoding process start")
        if reaction.msg_type == "SupportedAppProtocol":
            exi = self.message_handler.supported_app_to_exi(xml)
        elif reaction.msg_type == "DC":
            exi = self.message_handler.v2g_dc_msg_to_exi(xml)
        elif reaction.msg_type == "Common":
            exi = self.message_handler.v2g_common_msg_to_exi(xml)
        else:
            raise Exception("Unknown message type")
        logger.debug("Encoded EXI message: " + hexdump.dump(exi, len(exi), ' '))
        if isinstance(reaction, PauseSession):
            # TODO
            raise NotImplementedError
        elif isinstance(reaction, TerminateSession):
            self.session.reset_message_timer()
            self.session.reset_sequence_timer()
            self.transport.write(bytes(EXIMessage()/EXIPayload(payloadContent=exi)))
            logger.info("Charging session terminated.")
        elif isinstance(reaction, SendMessage):
            self.session.reset_message_timer()
            self.session.sequence_timer.start()
            if reaction.msg_type == "DC":
                message = bytes(EXIDCMessage() / EXIPayload(payloadContent=exi))
            elif reaction.msg_type == "SupportedAppProtocol":
                message = bytes(SupportedAppMessage()/EXIPayload(payloadContent=exi))
            elif reaction.msg_type == "Common":
                message = bytes(EXIMessage() / EXIPayload(payloadContent=exi))
            else:
                raise Exception("Unknown message type")
            self.transport.write(message)
        self.session.save_session_data(reaction.extra_data)

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, value):
        self.notify()
        self.__session = value

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        logger.info("Sent notification.")
        for observer in self._observers:
            observer.update(self)


def get_ssl_context(controller) -> ssl.SSLContext:
    """Returns an SSL context based on 15118-20 recommendations.

    :return: ssl.SSLContext -- the SSL settings for the TLS connection.
    """
    if SECURITY_PROTOCOL==0x10: # Check if TLS has been disabled for testing purposes
        return None
    else:
        context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH, cafile=EVCC_CERTIFICATE_AUTHORITY)
        # OpenSSL 1.1.1 has TLS 1.3 cipher suites enabled by default. The suites cannot be disabled with set_ciphers().
        # The line below loads the certificates chain that will be sent to the peer. It will be used for the TLS handshake.
        # Its private key is provided along with a passphrase that was used to encrypt it.
        context.load_cert_chain(SECC_CERTCHAIN, SECC_KEYFILE, PASSPHRASE)
        context.verify_mode = True
        return context


def get_tcp_server(controller, tcp_server_address: str, tcp_server_port: int):
    """Returns the TCP server used in the 15118 communication.

    :param controller: The controller that will handle the data.
    :param tcp_server_address: The server address.
    :param tcp_server_port: The server port.
    :return: server -- the created server
    """
    context = get_ssl_context(controller)
    loop = asyncio.get_event_loop()
    logger.info("Starting TCP server.")
    task = loop.create_server(lambda: TCPServerProtocol(controller), tcp_server_address, tcp_server_port, ssl=context)
    server = loop.run_until_complete(task)
    return server
