"""
.. module:: process_dc_cable_check_request
   :platform: Unix
   :synopsis: A module describing the DcCableCheck state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import DcEVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcCableCheckRes, MessageHeaderType, ResponseCodeType, ProcessingType
import time
import asyncio


class ProcessDcCableCheckRequest(DcEVSEState):
    def __init__(self):
        super(ProcessDcCableCheckRequest, self).__init__(name="ProcessDcCableCheckReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        asyncio.create_task(self.controller.state_machine.charge())
        extra_data = {}
        response = DcCableCheckRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if self.controller.state_machine.is_state_c():
            # See [V2G20-917]
            response.response_code = ResponseCodeType.OK
        else:
            # [V2G20-918]
            response.response_code = ResponseCodeType.FAILED
        response.evseprocessing = ProcessingType.FINISHED
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        return reaction
