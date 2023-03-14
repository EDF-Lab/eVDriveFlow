"""
.. module:: process_service_selection_request
   :platform: Unix
   :synopsis: A module describing the ServiceSelection state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceSelectionRes, MessageHeaderType, ResponseCodeType
import time


class ProcessServiceSelectionRequest(EVSEState):
    def __init__(self):
        super(ProcessServiceSelectionRequest, self).__init__(name="ProcessServiceSelectionReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = ServiceSelectionRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if payload.selected_energy_transfer_service.service_id == 6:
            response.response_code = ResponseCodeType.OK
            self.session_parameters.dc_bpt_selected = True
        elif payload.selected_energy_transfer_service.service_id == 2:
            response.response_code = ResponseCodeType.OK
            self.session_parameters.dc_bpt_selected = False
        else :
            response.response_code = ResponseCodeType.FAILED
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        return reaction
