"""
.. module:: process_service_discovery_request
   :platform: Unix
   :synopsis: A module describing the ServiceDiscovery state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceDiscoveryRes, MessageHeaderType, ResponseCodeType
import time


class ProcessServiceDiscoveryRequest(EVSEState):
    def __init__(self):
        super(ProcessServiceDiscoveryRequest, self).__init__(name="ProcessServiceDiscoveryReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = ServiceDiscoveryRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        response.service_renegotiation_supported = self.controller.data_model.service_renegotiation_supported
        response.energy_transfer_service_list = self.controller.data_model.energy_transfer_service_list
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        return reaction