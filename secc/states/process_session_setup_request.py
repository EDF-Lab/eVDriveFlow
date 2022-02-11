"""
.. module:: process_session_setup_request
   :platform: Unix
   :synopsis: A module describing the SessionSetup state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from secc.states.evse_state import EVSEState
from shared.xml_classes.common_messages import SessionSetupRes, MessageHeaderType, ResponseCodeType, EvsestatusType
import time


class ProcessSessionSetupRequest(EVSEState):
    def __init__(self):
        super(ProcessSessionSetupRequest, self).__init__(name="ProcessSessionSetupReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = SessionSetupRes()
        session_id = self.session_parameters.session_id
        response.header = MessageHeaderType(session_id=session_id, time_stamp=int(time.time()))
        # TODO: joining old session
        response.response_code = ResponseCodeType.OK_NEW_SESSION_ESTABLISHED
        evse_id = self.controller.data_model.evseid
        response.evseid = evse_id
        # Saving session data
        extra_data["session_id"] = session_id
        extra_data["evse_id"] = evse_id
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        return reaction




