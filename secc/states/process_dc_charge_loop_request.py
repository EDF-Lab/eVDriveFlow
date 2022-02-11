"""
.. module:: process_dc_charge_loop_request
   :platform: Unix
   :synopsis: A module describing the DcChargeLoop state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import time
from secc.states.evse_state import DcEVSEState
from shared.log import logger
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcChargeLoopRes, MessageHeaderType, ResponseCodeType
from shared.utils import float_to_dc_rational, rational_to_float, lower_rational


class ProcessDcChargeLoopRequest(DcEVSEState):
    def __init__(self):
        super(ProcessDcChargeLoopRequest, self).__init__(name="ProcessDcChargeLoopReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = DcChargeLoopRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        present_current = self.controller.data_model.evsepresent_current
        # In theory, if the EVSE has symmetrical parameters for charge/discharge, half of the operations here are not
        # needed. For more thoroughness, I decided to write all cases.
        if rational_to_float(present_current) < 0:
            evse_max_discharge_current = self.controller.data_model.evsemaximum_discharge_current
            ev_max_discharge_current = payload.bpt_dynamic_dc_clreq_control_mode.evmaximum_discharge_current
            current_limit = lower_rational(evse_max_discharge_current, ev_max_discharge_current)
        else:
            evse_max_charge_current = self.controller.data_model.evsemaximum_charge_current
            ev_max_charge_current = payload.bpt_dynamic_dc_clreq_control_mode.evmaximum_charge_current
            current_limit = lower_rational(evse_max_charge_current, ev_max_charge_current)
        if self.is_limit_achieved(current_limit, present_current):
            logger.warning("Current limit achieved!")
            response.evsecurrent_limit_achieved = True
            present_current = current_limit
        else:
            response.evsecurrent_limit_achieved = False
        response.evsepresent_current = present_current
        # Computing present_voltage: U_evse = R*I + U_ev
        present_voltage = rational_to_float(present_current) * self.controller.data_model.internal_resistance
        present_voltage += rational_to_float(payload.evpresent_voltage)
        present_voltage = float_to_dc_rational(present_voltage)
        voltage_limit = lower_rational(self.controller.data_model.evsemaximum_voltage,
                                       payload.bpt_dynamic_dc_clreq_control_mode.evmaximum_voltage)
        if self.is_limit_achieved(voltage_limit, present_voltage):
            logger.warning("Voltage limit achieved!")
            response.evsevoltage_limit_achieved = True
            present_voltage = voltage_limit
        else:
            response.evsevoltage_limit_achieved = False
        self.controller.data_model.evsepresent_voltage = present_voltage
        response.evsepresent_voltage = present_voltage

        power = rational_to_float(present_current) * rational_to_float(present_voltage)
        ev_max_discharge_power = payload.bpt_dynamic_dc_clreq_control_mode.evmaximum_discharge_power
        ev_max_charge_power = payload.bpt_dynamic_dc_clreq_control_mode.evmaximum_charge_power
        self.controller.data_model.evmaximum_discharge_power = ev_max_discharge_power
        self.controller.data_model.evmaximum_charge_power = ev_max_charge_power
        if power < 0:
            evse_max_discharge_power = self.controller.data_model.evsemaximum_discharge_power
            power_limit = lower_rational(evse_max_discharge_power, ev_max_discharge_power)
        else:
            evse_max_charge_power = self.controller.data_model.evsemaximum_charge_power
            power_limit = lower_rational(evse_max_charge_power, ev_max_charge_power)
        power = float_to_dc_rational(power)
        if self.is_limit_achieved(power_limit, power):
            logger.warning("Power limit achieved!")
            response.evsepower_limit_achieved = True
            power = power_limit
        else:
            response.evsepower_limit_achieved = False
        self.controller.data_model.evsepresent_power = power
        display_parameters = payload.display_parameters
        self.controller.data_model.update_charging_status(display_parameters.present_soc,
                                                          display_parameters.battery_energy_capacity, power)
        # power is one step late :'(
        response.bpt_dynamic_dc_clres_control_mode = self.controller.data_model.get_bpt_dynamic_dc_clres_control_mode()
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        return reaction

    @staticmethod
    def is_limit_achieved(limit, value):
        return limit == lower_rational(limit, value)
