"""
.. module:: wait_for_service_discovery_response
   :platform: Unix
   :synopsis: A module describing the ServiceDiscovery state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceDetailReq, MessageHeaderType
import time


class WaitForServiceDiscoveryResponse(EVState):
    def __init__(self):
        super(WaitForServiceDiscoveryResponse, self).__init__(name="WaitForServiceDiscoveryRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = ServiceDetailReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        for service in payload.energy_transfer_service_list.service:
            if service.service_id in self.controller.data_model.supported_service_ids.service_id:
                # TODO input from HMI
                request.service_id = 6
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = request
        return reaction
