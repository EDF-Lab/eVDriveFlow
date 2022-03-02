"""
.. module:: process_pre_charge_request
   :platform: Unix
   :synopsis: A module describing the PreCharge state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import DcEVSEState
from shared.log import logger
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcPreChargeRes, MessageHeaderType, ResponseCodeType
import time


class ProcessDcPreChargeRequest(DcEVSEState):
    def __init__(self):
        super(ProcessDcPreChargeRequest, self).__init__(name="ProcessDcPreChargeReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = DcPreChargeRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        present_voltage = self.controller.data_model.evsepresent_voltage
        target_voltage = payload.evtarget_voltage
        if present_voltage != target_voltage:
            self.controller.data_model.evsepresent_voltage = target_voltage
            # TODO: ramping up the voltage physically
        response.evsepresent_voltage = target_voltage
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        reaction.msg_type = "DC"
        return reaction
