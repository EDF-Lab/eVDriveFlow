"""
.. module:: tcp_client
   :platform: Unix
   :synopsis: A module that implements 15118 TCP client.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from asyncio import transports
from typing import Optional
import ssl
import sys
from shared.session_handler import SessionHandler
from shared.payloads import EXIPayload
from shared.message_handling import MessageHandler
from shared.reaction_message import PauseSession, TerminateSession, SendMessage
from shared.xml_classes.app_protocol import SupportedAppProtocolReq
from shared.global_values import EVCC_CERTCHAIN, EVCC_KEYFILE, PASSPHRASE, SECC_CERTIFICATE_AUTHORITY, SECURITY_PROTOCOL
import asyncio
from shared.messages import EXIMessage, V2GTPMessage, SupportedAppMessage, EXIDCMessage
from shared.log import logger
from evcc.event_handler import KeyboardListener
from shared.xml_classes.common_messages import SessionStopReq, MessageHeaderType, ChargingSessionType
import time
import hexdump


class TCPClientProtocol(asyncio.Protocol):
    """This is the TCP protocol used by EV client to communicate with the SECC.

    """

    def __init__(self, session_handler):
        """Basic constructor.

        :param session_handler: The session handler that will manage the communication sessions.
        """
        self.transport = None
        self.session_handler = session_handler
        self.session = self.session_handler.current_session
        self.message_handler = MessageHandler()
        self.__stop_session = False
        self.kb_listener = KeyboardListener(self.ainput)
        super(TCPClientProtocol, self).__init__()

    def get_tls_version(self):
        return str(self.transport._ssl_protocol._extra['cipher'][1])

    def get_negotiated_cipher(self):
        return str(self.transport._ssl_protocol._extra['cipher'][0])

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.session.update_timers()
        self.transport = transport
        logger.info("Connection made with %s. Starting new communication session.",
                    self.transport.get_extra_info("peername"))
        if SECURITY_PROTOCOL == 0x10: # Check if TLS has been disabled

            logger.info("\n\n\n TLS DISABLED \n\n\n")
        else:
            logger.info("\n\n\n TLS Session established: TLS Version: " + self.get_tls_version() + "\n Cipher suite: " +
                        self.get_negotiated_cipher() + '\n\n\n')

        xml_string, message, request = self.build_supported_app_protocol_message()
        self.session.message_timer.start()
        self.send(xml_string, message, request)

    def data_received(self, data: bytes) -> None:
        addr = self.transport.get_extra_info('peername')
        logger.info("Received response from %s.", addr)
        if self.session.state == "WaitForSupportedAppProtocolRes":
            packet = SupportedAppMessage(data)
        elif "Dc" in self.session.state:
            packet = EXIDCMessage(data)
        else:
            packet = EXIMessage(data)
        self.process_incoming_message(packet)

    def eof_received(self) -> Optional[bool]:
        logger.info('Received EOF.')
        if self.transport.can_write_eof():
            self.transport.write_eof()
            loop = asyncio.get_event_loop()
            loop.stop()

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            logger.error("%s.", exc)
        else:
            logger.info('Closing connection.')
        super().connection_lost(exc)

    def process_incoming_message(self, v2gtp_message: V2GTPMessage) -> None:
        """Processes the incoming message.

        :param v2gtp_message: The incoming message
        :return:
        """
        if self.message_handler.is_valid(v2gtp_message):
            payload = v2gtp_message.payload.getfieldval("payloadContent")
            message_type = v2gtp_message.get_payload_type()
            logger.info("Payload type: " + str(message_type))
            logger.debug("Received EXI msg to be decoded: " + hexdump.dump(payload, len(payload), ' '))
            if message_type == 0x8001:
                xml = self.message_handler.exi_to_supported_app(payload)
            elif message_type == 0x8004:
                xml = self.message_handler.exi_to_v2g_dc_msg(payload)
            elif message_type == 0x8002:
                xml = self.message_handler.exi_to_v2g_common_msg(payload)
            else:
                raise Exception("Unknown payload type")
            logger.info("Message successfully decoded " + xml)
            xml_object = self.message_handler.unmarshall(xml)
            request_type = type(xml_object).__name__
            logger.info("Received %s.", request_type)
            self.session.controller.data_model.state = request_type
            self.session.reset_message_timer()
            self.session.sequence_timer.start()
            reaction = self.get_current_state().process_payload(xml_object)
            self.process_reaction(reaction)
        else:
            self.process_reaction(TerminateSession())

    def process_reaction(self, reaction) -> None:
        """Depending on the reaction generated by the incoming message, will send an answer to the server.

        :param reaction: The reaction resulting from the incoming message.
        :return:
        """
        if isinstance(reaction, PauseSession):
            pass
        elif isinstance(reaction, TerminateSession):
            # if self.transport.can_write_eof():
            # can_write_eof doesn't work in TLS connections so we can't cut it off the by sending an EOF
            self.session.reset_sequence_timer()
            self.session.reset_message_timer()
            self.transport.close()
            asyncio.get_event_loop().stop()
        elif isinstance(reaction, SendMessage):
            if self.session.session_parameters.stop_session and \
                    self.session.is_state_exitable(self.get_current_state()):
                xml_string, message, request = self.build_session_stop_message()
                logger.debug("XML message to be sent: " + xml_string)
            else:
                request = reaction.message
                xml_string = self.message_handler.marshall(request)
                logger.debug("XML message to be sent: " + xml_string)
                if reaction.msg_type == "DC":
                    exi = self.message_handler.v2g_dc_msg_to_exi(xml_string)
                    message = bytes(EXIDCMessage() / EXIPayload(payloadContent=exi))
                elif reaction.msg_type == "Common":
                    exi = self.message_handler.v2g_common_msg_to_exi(xml_string)
                    message = bytes(EXIMessage() / EXIPayload(payloadContent=exi))
                elif reaction.msg_type == "SupportedAppProtocol":
                    exi = self.message_handler.supported_app_to_exi(xml_string)
                    message = bytes(SupportedAppMessage() / EXIPayload(payloadContent=exi))
                else:
                    raise Exception("Unknown message type")
                logger.debug("Encoded EXI message: " + hexdump.dump(exi, len(exi), ' '))

            self.session.reset_sequence_timer()
            self.session.message_timer.start()
            self.send(xml_string, message, request)
            self.session.save_session_data(reaction.extra_data)
            self.session.next_state()

    def build_supported_app_protocol_message(self) -> SupportedAppMessage:
        """Builds the SupportedAppProtocolMessage.

        :return: SupportedAppMessage -- the actual message.
        """
        protocols_list = self.session.controller.data_model.supported_app_protocols
        # Saving supported app protocols in session
        self.session.session_parameters.supported_app_protocols = protocols_list
        request = SupportedAppProtocolReq(protocols_list)
        xml_string = self.message_handler.marshall(request)
        exi = self.message_handler.supported_app_to_exi(xml_string)
        message = SupportedAppMessage() / EXIPayload(payloadContent=exi)
        return xml_string, bytes(message), request

    def build_session_stop_message(self) -> EXIMessage:
        """Builds a SessionStopMessage.

        :return: SessionStopMessage -- the message to stop a session.
        """
        request = SessionStopReq()
        request.header = MessageHeaderType(self.session.session_parameters.session_id, int(time.time()))
        request.charging_session = ChargingSessionType.TERMINATE
        xml_string = self.message_handler.marshall(request)
        exi = self.message_handler.v2g_common_msg_to_exi(xml_string)
        message = EXIMessage() / EXIPayload(payloadContent=exi)
        return xml_string, bytes(message), request

    async def ainput(self) -> None:
        """Awaits the 'return' key press to stop a session.

        :return:
        """
        # await asyncio.get_event_loop().run_in_executor(None, lambda s=string: sys.stdout.write(s + ' '))
        await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        await self.set_stop()


    def set_stop(self) -> None:
        """Awaits the 'return' key press to stop a session.

        :return:
        """
        self.session.session_parameters.stop_session = True
        self.session.session_parameters.charging = False
        logger.warning("Session stop has been requested.")

    def get_current_state(self) -> str:
        """Returns the current 15118 state.

        :return: str - the current state.
        """
        return self.session.get_state(self.session.state)

    def send(self, xml_string, message, request):
        """Sends a message and decorates it logger messages about the contents.

        :param xml_string: The XML string.
        :param message: The bytes type message.
        :param request: The XML object.
        :return:
        """
        self.transport.write(message)
        logger.info("Sent %s.", type(request).__name__)


def get_ssl_context(controller) -> ssl.SSLContext:
    """Returns an SSL context suitable for 15118 communication.

    :return: ssl.SSLContext -- the security context.
    """
    if SECURITY_PROTOCOL == 0x10:
        return None
    else:
        # OpenSSL 1.1.1 has TLS 1.3 cipher suites enabled by default. The suites cannot be disabled with set_ciphers().
        context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=SECC_CERTIFICATE_AUTHORITY)
        # The line below loads the certificates chain that will be sent to the peer. It will be used for the TLS handshake.
        # Its private key is provided along with a passphrase that was used to encrypt it.
        context.load_cert_chain(EVCC_CERTCHAIN, EVCC_KEYFILE, PASSPHRASE)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = False
        return context


def get_tcp_client(tcp_server_address: str, tcp_server_port: int, session_handler: SessionHandler):
    """Returns the TCP client used in the 15118 communication.

    :param tcp_server_address: The TCP server address.
    :param tcp_server_port: The TCP server port.
    :param session_handler: The session handler that manages the sessions.
    :return: transport, protocol -- the objects associated with the TCP connection.
    """
    loop = asyncio.get_event_loop()
    logger.info("Starting TCP client.")
    task = loop.create_connection(lambda: TCPClientProtocol(session_handler), tcp_server_address,
                                  tcp_server_port, ssl=get_ssl_context(session_handler.current_session.controller))
    # TODO: set tcp client port using config file
    transport, protocol = loop.run_until_complete(task)

    return transport, protocol



