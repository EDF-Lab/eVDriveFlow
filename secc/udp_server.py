"""
.. module:: udp_server
   :platform: Unix
   :synopsis: A module that implements 15118 udp server.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import asyncio
import socket
import struct
from asyncio import transports
from typing import Tuple, Optional
from shared.global_values import LOCAL_LINK_MULTICAST_ADDRESS, UDP_SERVER_PORT
from shared.messages import SDPMessage, SDPResPayload
from shared.log import logger
from shared.message_handling import MessageHandler


class UDPServerProtocol(asyncio.DatagramProtocol):
    """This is the protocol used by the SECC discovery protocol server.

    """
    def __init__(self, tcp_server_address, tcp_server_port):
        """Basic constructor.

        :param tcp_server_address: The TCP server address that will be made available to the EV.
        :param tcp_server_port: The TCP server port that will be made available to the EV.
        """
        super(UDPServerProtocol, self).__init__()
        self.transport = None
        self.message = bytes(SDPMessage() / SDPResPayload(TargetAddress=tcp_server_address,
                                                          TargetPort=tcp_server_port))
        self.message_handler = MessageHandler()

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        logger.info("Waiting for discovery request...")

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        logger.info("Received request from %s.", addr)
        packet = SDPMessage(data)
        if self.message_handler.is_valid(packet):
            # TODO: add verification for payload
            self.transport.sendto(self.message, addr)
            logger.info("Sent response to %s.", addr)

    def error_received(self, exc: Exception) -> None:
        logger.error("Error received, exception: %s.", exc)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            logger.error("Connection lost, exception :%s.", exc)
            logger.info("Closing transport.")


def get_udp_server(tcp_server_address, tcp_server_port):
    """Returns UDP server used in 15118 communication.

    :param tcp_server_address: The TCP server address.
    :param tcp_server_port: The TCP server port.
    :return: transport, protocol -- the objects associated with the UDP connection.
    """
    loop = asyncio.get_event_loop()
    addrinfo = socket.getaddrinfo(LOCAL_LINK_MULTICAST_ADDRESS, None)[0]
    # Creating custom socket for UDP multicasting (server side)
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    # Setting options for socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # SOL_SOCKET describes the socket layer itself,
    # SO_REUSEADDR tells to the kernel to reuse port if is waiting for connection, last argument is length of buffer
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Joining the multicasting group so that the server can listen to the casters
    sock.bind(('', UDP_SERVER_PORT))
    mreq = group_bin + struct.pack('@I', 0)
    # Setting options for IPV6 group
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
    logger.info("Starting UDP server.")
    task = loop.create_datagram_endpoint(lambda: UDPServerProtocol(tcp_server_address, tcp_server_port), sock=sock)
    transport, protocol = loop.run_until_complete(task)
    return transport, protocol
