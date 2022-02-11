"""
.. module:: evse_state
   :platform: Unix
   :synopsis: A module describing EVSE states.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from abc import abstractmethod
from shared.reaction_message import ReactionToIncomingMessage
from shared.state import V2GState
from shared.global_values import SECC_ONGOING_TIMEOUT, SECC_SEQUENCE_TIMEOUT, SECC_ONGOING_PERFORMANCE_TIME, \
    SECC_MSG_PERFORMANCE_TIME, DC_SECC_MSG_PERFORMANCE_TIME, DC_SECC_SEQUENCE_TIMEOUT


class EVSEState(V2GState):
    """This is a class that represents an EVSE state.

    """
    def __init__(self, *args, **kwargs):
        super(EVSEState, self).__init__(*args, **kwargs)
        self.ongoing_timeout = SECC_ONGOING_TIMEOUT
        self.ongoing_perf_time = SECC_ONGOING_PERFORMANCE_TIME
        self.timeout = SECC_SEQUENCE_TIMEOUT
        for key, value in SECC_MSG_PERFORMANCE_TIME.items():
            if key in self.name:
                self.seq_perf_time = value

    @abstractmethod
    def process_payload(self, payload) -> ReactionToIncomingMessage:
        pass


class DcEVSEState(V2GState):
    """This is a class that represents a DC EVSE state.

    """
    def __init__(self, *args, **kwargs):
        super(DcEVSEState, self).__init__(*args, **kwargs)
        self.ongoing_timeout = SECC_ONGOING_TIMEOUT
        self.ongoing_perf_time = SECC_ONGOING_PERFORMANCE_TIME
        if "DcChargeLoopRes" in self.name:
            self.timeout = DC_SECC_SEQUENCE_TIMEOUT["DcChargeLoopRes"]
        else:
            self.timeout = SECC_SEQUENCE_TIMEOUT
        for key, value in DC_SECC_MSG_PERFORMANCE_TIME.items():
            if key in self.name:
                self.seq_perf_time = value

    @abstractmethod
    def process_payload(self, payload) -> ReactionToIncomingMessage:
        pass
