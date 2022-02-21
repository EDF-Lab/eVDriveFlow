"""
.. module:: wait_for_dc_cable_check_response
   :platform: Unix
   :synopsis: A module describing the DcCableCheck state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import DcEVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcPreChargeReq, MessageHeaderType, RationalNumberType, ProcessingType
import time


class WaitForDcCableCheckResponse(DcEVState):
    def __init__(self):
        super(WaitForDcCableCheckResponse, self).__init__(name="WaitForDcCableCheckRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = DcPreChargeReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        request.evprocessing = ProcessingType.ONGOING
        request.evpresent_voltage = self.controller.data_model.evpresent_voltage  # 0V
        request.evtarget_voltage = RationalNumberType(0, 330)  # set evse and ev to this value
        self.session_parameters.processing = True
        reaction = SendMessage()
        reaction.message = request
        reaction.extra_data = extra_data
        reaction.msg_type = "DC"
        return reaction
