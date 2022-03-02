from abc import abstractmethod

from shared.log import logger
from shared.reaction_message import ReactionToIncomingMessage
from shared.state import V2GState
from shared.global_values import EVCC_MSG_TIMEOUT, EVCC_ONGOING_TIMEOUT, EVCC_ONGOING_PERFORMANCE_TIME, \
    EVCC_SEQUENCE_PERFORMANCE_TIME, DC_EVCC_SEQUENCE_PERFORMANCE_TIME, DC_EVCC_MSG_TIMEOUT


class EVState(V2GState):
    def __init__(self, *args, **kwargs):
        super(EVState, self).__init__(*args, **kwargs)
        self.seq_perf_time = EVCC_SEQUENCE_PERFORMANCE_TIME
        self.ongoing_timeout = EVCC_ONGOING_TIMEOUT
        self.ongoing_perf_time = EVCC_ONGOING_PERFORMANCE_TIME
        for key, value in EVCC_MSG_TIMEOUT.items():
            if key[:-3] in self.name:
                self.timeout = value

    @abstractmethod
    def process_payload(self, payload) -> ReactionToIncomingMessage:
        pass


class DcEVState(V2GState):
    def __init__(self, *args, **kwargs):
        super(DcEVState, self).__init__(*args, **kwargs)
        if "DcChargeLoop" in self.name:
            self.seq_perf_time = DC_EVCC_SEQUENCE_PERFORMANCE_TIME["DcChargeLoopReq"]
        else:
            self.seq_perf_time = EVCC_SEQUENCE_PERFORMANCE_TIME
        self.ongoing_timeout = EVCC_ONGOING_TIMEOUT
        self.ongoing_perf_time = EVCC_ONGOING_PERFORMANCE_TIME
        for key, value in DC_EVCC_MSG_TIMEOUT.items():
            if key[:-3] in self.name:
                self.timeout = value

    @abstractmethod
    def process_payload(self, payload) -> ReactionToIncomingMessage:
        pass
