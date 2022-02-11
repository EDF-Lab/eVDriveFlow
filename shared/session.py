"""
.. module:: session
   :platform: Unix
   :synopsis: A module that dictates how a charging session behaves.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import configparser
from dataclasses import dataclass
from transitions.extensions.asyncio import Machine

from shared.controller import ControllerInterface
from shared.timer import MessageTimer, SequenceTimer
from shared.message_handling import MessageHandler


class CommunicationSession(Machine):
    """This is a charging session's implementation as understood from 15118.

    """
    def __init__(self, controller: ControllerInterface, *args, **kwargs):
        """Basic constructor.

        :param controller: The controller that will handle the data and the view.
        :param args:
        :param kwargs:
        """
        self.message_handler = MessageHandler()
        self.__sequence_timer = None
        self.__message_timer = None
        self.__controller = controller
        self.__session_parameters = SessionParameters()
        super(CommunicationSession, self).__init__(*args, **kwargs)

    def stop_session(self):
        pass

    def pause_session(self):
        pass

    def _get_config_params(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        params = config["PARAMETERS"]
        return params

    def save_session_data(self, extra_data):
        if extra_data:
            for key, value in extra_data.items():
                setattr(self.session_parameters, key, value)

    @property
    def sequence_timer(self):
        return self.__sequence_timer

    @sequence_timer.setter
    def sequence_timer(self, value):
        self.__sequence_timer = value

    @property
    def message_timer(self):
        return self.__message_timer

    @message_timer.setter
    def message_timer(self, value):
        self.__message_timer = value

    def update_sequence_timer(self):
        current_state = self.get_state(self.state)
        self.sequence_timer = SequenceTimer(timeout=current_state.seq_perf_time)

    def reset_sequence_timer(self):
        if self.sequence_timer.task:
            self.sequence_timer.cancel()
        self.update_sequence_timer()

    def update_message_timer(self):
        current_state = self.get_state(self.state)
        self.message_timer = MessageTimer(timeout=current_state.timeout)

    def reset_message_timer(self):
        if self.message_timer.task:
            self.message_timer.cancel()
        self.update_message_timer()

    def update_timers(self):
        self.update_sequence_timer()
        self.update_message_timer()

    @property
    def controller(self):
        return self.__controller

    @property
    def session_parameters(self):
        return self.__session_parameters

    @session_parameters.setter
    def session_parameters(self, value):
        self.__session_parameters = value


@dataclass
class SessionParameters:
    """This is a dataclass that will hold any useful information for the charging session.

    """
    session_id: bytes = None
    ip_address: str = None
    port: int = None
