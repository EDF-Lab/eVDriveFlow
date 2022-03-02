"""
.. module:: session_handler
   :platform: Unix
   :synopsis: A module that will manage charging sessions.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.session import CommunicationSession
from abc import abstractmethod


class SessionHandler:
    """This a class that will handle the different charging sessions during the V2G communication.

    """
    def __init__(self):
        """Basic constructor.

        """
        self.__sessions = []
        self.__current_session = None
        self.__interface = None
        self.__tcp_port = None

    @abstractmethod
    def get_config(self):
        """Gets the needed configuration to run a SessionHandler.

        :return:
        """
        pass

    @abstractmethod
    def start_new_session(self, controller):
        """Starts a new communication session.

        :param controller: The controller that will handle the data.
        :return:
        """
        pass

    def set_network_parameters(self):
        """Sets the settings according to the configuration file.

        :return:
        """
        config = self.get_config()["NETWORK"]
        self.interface = config["interface"]
        self.tcp_port = config.getint("tcp_port")

    @property
    def current_session(self):
        return self.__current_session

    @current_session.setter
    def current_session(self, session: CommunicationSession):
        if session not in self.__sessions:
            self.__sessions.append(session)
        self.__current_session = session

    @property
    def sessions(self):
        return self.__sessions

    @sessions.setter
    def sessions(self, sessions: [CommunicationSession]):
        self.__sessions = sessions

    @property
    def interface(self):
        return self.__interface

    @interface.setter
    def interface(self, value):
        self.__interface = value

    @property
    def tcp_port(self):
        return self.__tcp_port

    @tcp_port.setter
    def tcp_port(self, value):
        self.__tcp_port = value
