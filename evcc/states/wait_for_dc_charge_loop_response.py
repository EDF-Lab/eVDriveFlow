"""
.. module:: wait_for_dc_charge_loop_response
   :platform: Unix
   :synopsis: A module describing the DcChargeLoop state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import DcEVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
import time
from shared.xml_classes.common_messages import PowerDeliveryReq, ChargeProgressType, ProcessingType, MessageHeaderType
from shared.xml_classes.dc import DcChargeLoopReq, MessageHeaderType as DcMessageHeaderType, DisplayParametersType


class WaitForDcChargeLoopResponse(DcEVState):
    def __init__(self):
        super(WaitForDcChargeLoopResponse, self).__init__(name="WaitForDcChargeLoopRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        reaction = SendMessage()
        if self.session_parameters.charging:
            if hasattr(payload.bpt_dynamic_dc_clres_control_mode, "departure_time"):
                self.controller.data_model.departure_time = payload.bpt_dynamic_dc_clres_control_mode.departure_time
            if hasattr(payload.bpt_dynamic_dc_clres_control_mode, "target_soc"):
                self.controller.data_model.target_soc = payload.bpt_dynamic_dc_clres_control_mode.target_soc
            request = DcChargeLoopReq()
            new_timestamp = time.time()
            old_timestamp = self.controller.data_model.timestamp
            timestep = new_timestamp - old_timestamp
            self.controller.data_model.timestamp = new_timestamp
            request.header = DcMessageHeaderType(self.session_parameters.session_id, int(new_timestamp))
            self.controller.data_model.update_charging_status(payload.evsepresent_current,
                                                              payload.evsepresent_voltage, timestep)
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
            reaction.msg_type = "DC"
        else:
            request = self.build_power_delivery_message()
            reaction.msg_type = "Common"

        reaction.message = request
        reaction.extra_data = extra_data
        return reaction

    def build_power_delivery_message(self):
        request = PowerDeliveryReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        request.charge_progress = ChargeProgressType.STOP
        request.evprocessing = ProcessingType.FINISHED
        return request