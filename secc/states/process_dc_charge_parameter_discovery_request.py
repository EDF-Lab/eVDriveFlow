"""
.. module:: process_dc_charge_parameter_discovery_request
   :platform: Unix
   :synopsis: A module describing the DcChargeParameterDiscovery state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import DcEVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import DcChargeParameterDiscoveryRes, ResponseCodeType, MessageHeaderType
import time


class ProcessDcChargeParameterDiscoveryRequest(DcEVSEState):
    def __init__(self):
        super(ProcessDcChargeParameterDiscoveryRequest, self).__init__(name="ProcessDcChargeParameterDiscoveryReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        controller = self.controller
        response = DcChargeParameterDiscoveryRes()
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))

        if self.session_parameters.dc_bpt_selected == True:
            ev_data = payload.bpt_dc_cpdreq_energy_transfer_mode
            controller.data_model.evmaximum_discharge_power = ev_data.evmaximum_discharge_power
            response.bpt_dc_cpdres_energy_transfer_mode = controller.data_model.get_bpt_dc_cpdres_energy_transfer_mode()
        else :
            ev_data = payload.dc_cpdreq_energy_transfer_mode
            controller.data_model.evmaximum_charge_power = ev_data.evmaximum_charge_power
            response.dc_cpdres_energy_transfer_mode = controller.data_model.get_dc_cpdres_energy_transfer_mode()

        if hasattr(ev_data, "departure_time"):
            controller.data_model.departure_time = ev_data.departure_time
        if hasattr(ev_data, "target_soc"):
            controller.data_model.target_soc = ev_data.target_soc
        # TODO: handle ev data, only max power is handled now for the hmi
        response.response_code = ResponseCodeType.OK
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "DC"
        return reaction
