"""
.. module:: state
   :platform: Unix
   :synopsis: A module that details a 15118 state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from abc import abstractmethod
from transitions import State
from shared.messages import EXIMessage, EXIDCMessage
from shared.payloads import EXIPayload
from shared.reaction_message import ReactionToIncomingMessage
from shared.message_handling import MessageHandler


class V2GState(State):
    """This a class that will hold everything everything needed in a 15118 state.

    """
    def __init__(self, *args, **kwargs):
        super(V2GState, self).__init__(*args, **kwargs)
        self.__seq_perf_time = 0
        self.__ongoing_perf_time = 0
        self.__timeout = 0
        self.__ongoing_timeout = 0
        self.message_handler = MessageHandler()
        self.__session = None

    def _build_message(self, message):
        self.message_handler.marshall(message)
        exi = self.message_handler.v2g_common_msg_to_exi()
        packet = EXIMessage() / EXIPayload(payloadContent=exi)
        return packet

    @abstractmethod
    def process_payload(self, payload) -> ReactionToIncomingMessage:
        """Processes the payload and readies the next message.

        :param payload: The data that will be processed.
        :return: ReactionToIncomingMessage -- the reaction the processed data.
        """
        pass

    @property
    def seq_perf_time(self):
        return self.__seq_perf_time

    @seq_perf_time.setter
    def seq_perf_time(self, value):
        self.__seq_perf_time = value

    @property
    def ongoing_timeout(self):
        return self.__ongoing_timeout

    @ongoing_timeout.setter
    def ongoing_timeout(self, value):
        self.__ongoing_timeout = value

    @property
    def ongoing_perf_time(self):
        return self.__ongoing_perf_time

    @ongoing_perf_time.setter
    def ongoing_perf_time(self, value):
        self.__ongoing_perf_time = value

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        self.__timeout = value

    @property
    def ongoing_timeout(self):
        return self.__ongoing_timeout

    @ongoing_timeout.setter
    def ongoing_timeout(self, value):
        self.__ongoing_timeout = value

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, value):
        self.__session = value
