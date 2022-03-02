"""
.. module:: evse_session_handler
   :platform: Unix
   :synopsis: A module that implements the server's side session_handler.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.session_handler import SessionHandler
from secc.udp_server import get_udp_server
from secc.tcp_server import get_tcp_server
import netifaces
from configparser import ConfigParser


class EVSESessionHandler(SessionHandler):
    """This is the class representing the EVSE session handler.

    """
    def __init__(self):
        super(EVSESessionHandler, self).__init__()
        self.set_network_parameters()

    def get_config(self):
        config = ConfigParser()
        config.read("evse_config.ini")
        return config

    def start_new_session(self, controller):
        tcp_server_address = self.get_tcp_server_address()
        tcp_server_port = self.tcp_port
        get_udp_server(tcp_server_address, tcp_server_port)
        get_tcp_server(controller, tcp_server_address, tcp_server_port)

    def get_tcp_server_address(self):
        """Gets a TCP server address from a specified interface set in the configuration file.

        :return:
        """
        return netifaces.ifaddresses(self.interface)[netifaces.AF_INET6][0]["addr"]
