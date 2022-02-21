"""
.. module:: process_authorization_request
   :platform: Unix
   :synopsis: A module describing the Authorization state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import AuthorizationRes, ResponseCodeType, ProcessingType, MessageHeaderType
import time


class ProcessAuthorizationRequest(EVSEState):
    def __init__(self):
        super(ProcessAuthorizationRequest, self).__init__(name="ProcessAuthorizationReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = AuthorizationRes()
        response.response_code = ResponseCodeType.OK
        response.evseprocessing = ProcessingType.FINISHED
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        reaction.msg_type = "Common"
        return reaction
