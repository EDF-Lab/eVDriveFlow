"""
.. module:: wait_for_dc_welding_detection_response
   :platform: Unix
   :synopsis: A module describing the WeldingDetection state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import DcEVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import SessionStopReq, MessageHeaderType, ChargingSessionType
import time


class WaitForDcWeldingDetectionResponse(DcEVState):
    def __init__(self):
        super(WaitForDcWeldingDetectionResponse, self).__init__(name="WaitForDcWeldingDetectionRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = SessionStopReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        request.charging_session = ChargingSessionType.TERMINATE
        request.evtermination_code = "End_of_charge"
        request.evtermination_explanation = "End_of_charge"
        reaction = SendMessage()
        reaction.message = request
        return reaction
