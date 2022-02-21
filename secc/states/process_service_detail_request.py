"""
.. module:: process_service_detail_request
   :platform: Unix
   :synopsis: A module describing the ServiceDetail state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ServiceDetailRes, MessageHeaderType, ResponseCodeType
import time


class ProcessServiceDetailRequest(EVSEState):
    def __init__(self):
        super(ProcessServiceDetailRequest, self).__init__(name="ProcessServiceDetailReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = ServiceDetailRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        response.service_id = payload.service_id
        extra_data["selected_service_id"] = payload.service_id
        response.service_parameter_list = self.controller.data_model.services[str(payload.service_id)]
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        return reaction
