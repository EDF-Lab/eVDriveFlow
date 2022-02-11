"""
.. module:: wait_for_power_delivery_response
   :platform: Unix
   :synopsis: A module describing the PowerDelivery state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.log import logger
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import ProcessingType, ResponseCodeType
from shared.xml_classes.dc import DcChargeLoopReq, MessageHeaderType, DisplayParametersType, DcWeldingDetectionReq
import asyncio
import time


class WaitForPowerDeliveryResponse(EVState):
    def __init__(self):
        super(WaitForPowerDeliveryResponse, self).__init__(name="WaitForPowerDeliveryRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        reaction = SendMessage()
        timestamp = time.time()
        if payload.evsestatus:
            asyncio.create_task(self.controller.state_machine.stop_charge())
            # See [V2G20-919]
            if payload.response_code == ResponseCodeType.OK:
                # maybe add a time.sleep() here
                logger.info("Current state is: %s.", self.controller.state_machine.state)
            request = DcWeldingDetectionReq()
            request.header = MessageHeaderType(self.session_parameters.session_id, int(timestamp))
            request.evprocessing = ProcessingType.ONGOING
        else:
            self.session_parameters.charging = True
            request = DcChargeLoopReq()
            request.header = MessageHeaderType(self.session_parameters.session_id, int(timestamp))
            request.bpt_dynamic_dc_clreq_control_mode = \
                self.controller.data_model.get_bpt_dynamic_dc_clreq_control_mode()
            request.display_parameters = DisplayParametersType(present_soc=self.controller.data_model.present_soc,
                                                               minimum_soc=self.controller.data_model.minimum_soc,
                                                               target_soc=self.controller.data_model.target_soc,
                                                               maximum_soc=self.controller.data_model.maximum_soc,
                                                               charging_complete=(
                                                                       self.controller.data_model.present_soc ==
                                                                       self.controller.data_model.target_soc),
                                                               battery_energy_capacity=
                                                               self.controller.data_model.battery_capacity)
            request.evpresent_voltage = self.controller.data_model.evpresent_voltage
            request.meter_info_requested = False
        reaction.message = request
        self.controller.data_model.timestamp = timestamp
        reaction.extra_data = extra_data
        return reaction
