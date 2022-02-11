"""
.. module:: wait_for_schedule_exchange_response
   :platform: Unix
   :synopsis: A module describing the ScheduleExchange state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import MessageHeaderType
import time
import asyncio

from shared.xml_classes.dc import DcCableCheckReq


class WaitForScheduleExchangeResponse(EVState):
    def __init__(self):
        super(WaitForScheduleExchangeResponse, self).__init__(name="WaitForScheduleExchangeRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        #if payload.evseprocessing == ProcessingType.FINISHED:
        # See [V2G20-912]
        if hasattr(payload.dynamic_seres_control_mode, "departure_time"):
            self.controller.data_model.departure_time = payload.dynamic_seres_control_mode.departure_time
        asyncio.create_task(self.controller.state_machine.charge())
        extra_data = {}
        request = DcCableCheckReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        reaction = SendMessage()
        reaction.message = request
        reaction.extra_data = extra_data
        return reaction
