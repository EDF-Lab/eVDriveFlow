"""
.. module:: wait_for_service_detail_response
   :platform: Unix
   :synopsis: A module describing the ServiceDetail state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceSelectionReq, MessageHeaderType, SelectedServiceType
import time


class WaitForServiceDetailResponse(EVState):
    def __init__(self):
        super(WaitForServiceDetailResponse, self).__init__(name="WaitForServiceDetailRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = ServiceSelectionReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if payload.service_id == 6:
            self.session_parameters.dc_bpt_selected = True
        elif payload.service_id == 2:
            self.session_parameters.dc_bpt_selected = False
        
        request.selected_energy_transfer_service = SelectedServiceType(payload.service_id, 1)
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = request
        reaction.msg_type = "Common"
        return reaction
