"""
.. module:: wait_for_authorization_response
   :platform: Unix
   :synopsis: A module describing the Authorization state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceDiscoveryReq, MessageHeaderType
import time


class WaitForAuthorizationResponse(EVState):
    def __init__(self):
        super(WaitForAuthorizationResponse, self).__init__(name="WaitForAuthorizationRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = ServiceDiscoveryReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        request.supported_service_ids = self.controller.data_model.supported_service_ids
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = request
        return reaction

