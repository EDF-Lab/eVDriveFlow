"""
.. module:: process_dc_welding_detection_request
   :platform: Unix
   :synopsis: A module describing the WeldingDetection state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import DcEVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcWeldingDetectionRes, MessageHeaderType, ResponseCodeType, RationalNumberType
import time

class ProcessDcWeldingDetectionRequest(DcEVSEState):
    def __init__(self):
        super(ProcessDcWeldingDetectionRequest, self).__init__(name="ProcessDcWeldingDetectionReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = DcWeldingDetectionRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if self.controller.state_machine.is_state_b():
            # [V2G20-921]
            response.response_code = ResponseCodeType.OK
        else:
            # [V2G20-922]
            response.response_code = ResponseCodeType.FAILED
        response.evsepresent_voltage = RationalNumberType(0, 300)
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        return reaction

