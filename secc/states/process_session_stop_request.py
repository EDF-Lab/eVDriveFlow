"""
.. module:: process_session_stop_request
   :platform: Unix
   :synopsis: A module describing the SessionStop state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, TerminateSession, SendMessage
from shared.xml_classes.common_messages import SessionStopRes, MessageHeaderType, ResponseCodeType
import time


class ProcessSessionStopRequest(EVSEState):
    def __init__(self):
        super(ProcessSessionStopRequest, self).__init__(name="ProcessSessionStopReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = SessionStopRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if self.controller.state_machine.is_B():
            # [V2G20-921]
            response.response_code = ResponseCodeType.OK
        else:
            # [V2G20-922]
            response.response_code = ResponseCodeType.FAILED
        reaction = TerminateSession()
        reaction.message = response
        reaction.extra_data = extra_data
        return reaction