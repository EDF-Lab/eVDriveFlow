"""
.. module:: process_schedule_exchange_request
   :platform: Unix
   :synopsis: A module describing the ScheduleExchange state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import MessageHeaderType, ResponseCodeType, ScheduleExchangeRes, ProcessingType
import time


class ProcessScheduleExchangeRequest(EVSEState):
    def __init__(self):
        super(ProcessScheduleExchangeRequest, self).__init__(name="ProcessScheduleExchangeReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = ScheduleExchangeRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        response.evseprocessing = ProcessingType.FINISHED
        if hasattr(payload.dynamic_sereq_control_mode, "departure_time"):
            self.controller.data_model.departure_time = payload.dynamic_sereq_control_mode.departure_time
        if hasattr(payload.dynamic_sereq_control_mode, "target_soc"):
            self.controller.data_model.target_soc = payload.dynamic_sereq_control_mode.target_soc
        response.dynamic_seres_control_mode = self.controller.data_model.get_dynamic_seres_control_mode()
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        return reaction
