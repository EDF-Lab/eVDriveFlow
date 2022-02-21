"""
.. module:: process_power_delivery_request
   :platform: Unix
   :synopsis: A module describing the PowerDelivery state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
import asyncio
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import PowerDeliveryRes, MessageHeaderType, ResponseCodeType, \
    ChargeProgressType, EvsestatusType, EvseNotificationType
import time


class ProcessPowerDeliveryRequest(EVSEState):
    def __init__(self):
        super(ProcessPowerDeliveryRequest, self).__init__(name="ProcessPowerDeliveryReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = PowerDeliveryRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        # TODO other cases
        if payload.charge_progress == ChargeProgressType.STOP:
            response.evsestatus = EvsestatusType(0, EvseNotificationType.TERMINATE)
            # See [V2G20-913]
            asyncio.create_task(self.controller.state_machine.stop_charge())
        return reaction
