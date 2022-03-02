"""
.. module:: ev_session_handler
   :platform: Unix
   :synopsis: A module that implements the client's side session_handler.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import asyncio
from shared.session_handler import SessionHandler
from evcc.ev_session import EVSession
from evcc.udp_client import get_udp_client
from evcc.tcp_client import get_tcp_client
from configparser import ConfigParser


class EVSessionHandler(SessionHandler):
    """This is a class that represents EV's session handler.

    """
    def __init__(self):
        super(EVSessionHandler, self).__init__()
        self.__udp_port = None
        self.set_network_parameters()

    def get_config(self):
        config = ConfigParser()
        config.read("ev_config.ini")
        return config

    def set_network_parameters(self):
        config = self.get_config()["NETWORK"]
        self.interface = config["interface"]
        self.tcp_port = config.getint("tcp_port")
        self.udp_port = config.getint("udp_port")

    def start_new_session(self, controller):
        self.current_session = EVSession(controller)
        udp_transport, udp_protocol = get_udp_client(self.udp_port, self.interface)
        
        interface = "%" + self.interface
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tcp_transport, tcp_protocol = \
            get_tcp_client(udp_protocol.tcp_server_address + interface, udp_protocol.tcp_server_port, self)

    @property
    def udp_port(self):
        return self.__udp_port

    @udp_port.setter
    def udp_port(self, value):
        self.__udp_port = value
