"""
.. module:: udp_client
   :platform: Unix
   :synopsis: A module that implements 15118 UDP client.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import asyncio
from asyncio.futures import Future
import socket
import struct
from asyncio import transports
import sys
from typing import Optional, Tuple
from shared.log import logger
from shared.global_values import LOCAL_LINK_MULTICAST_ADDRESS, UDP_SERVER_PORT
from shared.messages import SDPMessage, SDPReqPayload
from shared.message_handling import MessageHandler
import time


class UDPClientProtocol(asyncio.DatagramProtocol):
    """This is the protocol used by the SECC discovery protocol client.

    """
    def __init__(self):
        super(UDPClientProtocol, self).__init__()
        self.transport = None
        self.message = bytes(SDPMessage()/SDPReqPayload())
        self.message_handler = MessageHandler()
        self.tcp_server_address = None
        self.tcp_server_port = None
        self.number_of_SDP_REQ_sent = 0
        self._send_discovery_req_task = None

    def connection_made(self, transport: transports.BaseTransport) -> None:
        self.transport = transport
        sock = self.transport.get_extra_info('socket')
        addrinfo = socket.getaddrinfo(LOCAL_LINK_MULTICAST_ADDRESS, UDP_SERVER_PORT)[0]
        logger.info("Attempting to connect to %s.", addrinfo[4])
        # Modifying socket options so that multicasting is possible
        ttl = struct.pack('@i', 2)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl)
        # self.transport.sendto(self.message, (LOCAL_LINK_MULTICAST_ADDRESS, UDP_SERVER_PORT))
        # logger.info("Sent SECC discovery request.")
        self._send_discovery_req_task = asyncio.ensure_future(self.send_SDP_req())
        
        
    async def send_SDP_req(self):
        for _ in range(10):
            self.transport.sendto(self.message, (LOCAL_LINK_MULTICAST_ADDRESS, UDP_SERVER_PORT))
            logger.info("Sent SECC discovery request. " + str(self.number_of_SDP_REQ_sent))
            self.number_of_SDP_REQ_sent += 1
            await asyncio.sleep(3)
            
        print("No answer from UDP Server, limit of requests reached")
        sys.exit(1)

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        logger.info("Received response from %s.", addr)
        packet = SDPMessage(data)
        if self.message_handler.is_valid(packet):
            self.tcp_server_address = packet.payload.getfieldval("TargetAddress")
            self.tcp_server_port = packet.payload.getfieldval("TargetPort")
            logger.info("TCP server is reachable at (%s, %s).", packet.payload.getfieldval("TargetAddress"),
                        packet.payload.getfieldval("TargetPort"))
            if self._send_discovery_req_task:
                self._send_discovery_req_task.cancel()
            if self.transport:
                self.transport.close()
                logger.info("Closing connection.")
            current_loop = asyncio.get_event_loop()
            if current_loop.is_running():
                current_loop.stop()  # once valid message received, it UDP loop will be stopped
                print("loop for UDP client socket is running..attempting to close")

    def error_received(self, exc: Exception) -> None:
        logger.error("Error received, exception: %s.", exc)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc:
            logger.error("Connection lost, exception :%s.", exc)
        loop = asyncio.get_event_loop()
        loop.stop()


def get_udp_client(udp_port, interface):
    """Returns the UDP client used in 15118 communication.

    :param udp_port: The UDP port for the client.
    :param interface: The interface that will be used for the connection.
    :return: transport, protocol -- the objects associated with the UDP connection.
    """
    addrinfo = socket.getaddrinfo(LOCAL_LINK_MULTICAST_ADDRESS, None)[0]
    # Creating custom socket for UDP multicasting (client side)
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, str(interface + '\0').encode('utf-8'))
    sock.bind(("", udp_port))
    loop = asyncio.get_event_loop()
    logger.info("Starting UDP client.")
    task = loop.create_datagram_endpoint(UDPClientProtocol, sock=sock)
    transport, protocol = loop.run_until_complete(task)
    
    loop.run_forever() # This loop is keeped alive for waitting UDP datagram, once valid message received, it will be stopped
    return transport, protocol

