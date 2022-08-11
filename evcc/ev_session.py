"""
.. module:: ev_session
   :platform: Unix
   :synopsis: A module that implements the client's side communication session.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.wait_for_dc_cable_check_response import WaitForDcCableCheckResponse
from evcc.states.wait_for_dc_charge_parameter_discovery_response import WaitForDcChargeParameterDiscoveryResponse
from evcc.states.wait_for_dc_charge_loop_response import WaitForDcChargeLoopResponse
from evcc.states.wait_for_power_delivery_response import WaitForPowerDeliveryResponse
from evcc.states.wait_for_dc_pre_charge_response import WaitForDcPreChargeResponse
from evcc.states.wait_for_schedule_exchange_response import WaitForScheduleExchangeResponse
from evcc.states.wait_for_service_detail_response import WaitForServiceDetailResponse
from evcc.states.wait_for_service_discovery_response import WaitForServiceDiscoveryResponse
from evcc.states.wait_for_service_selection_response import WaitForServiceSelectionResponse
from evcc.states.wait_for_session_stop_response import WaitForSessionStopResponse
from evcc.states.wait_for_dc_welding_detection_response import WaitForDcWeldingDetectionResponse
from shared.log import logger
from states.wait_for_authorization_response import WaitForAuthorizationResponse
from states.wait_for_session_setup_response import WaitForSessionSetupResponse
from shared.session import CommunicationSession
from shared.session import SessionParameters
from dataclasses import dataclass
from states.wait_for_supported_app_protocol_response import WaitForSupportedAppProtocolResponse
from states.wait_for_authorization_setup_response import WaitForAuthorizationSetupResponse


class EVSession(CommunicationSession):
    """Represents a EV side communication session. Built with a state machine.

    """
    def __init__(self, controller):
        """Basic constructor.

        :param controller: The controller that will handle the data.
        """
        # Instantiation of every state
        initial_state = "initial_state"
        supported_app_protocol_state = WaitForSupportedAppProtocolResponse()
        session_setup_state = WaitForSessionSetupResponse()
        authorization_setup_state = WaitForAuthorizationSetupResponse()
        authorization_state = WaitForAuthorizationResponse()
        service_discovery_state = WaitForServiceDiscoveryResponse()
        service_detail_state = WaitForServiceDetailResponse()
        service_selection_state = WaitForServiceSelectionResponse()
        charge_parameter_discovery_state = WaitForDcChargeParameterDiscoveryResponse()
        schedule_exchange_state = WaitForScheduleExchangeResponse()
        cable_check_state = WaitForDcCableCheckResponse()
        pre_charge_state = WaitForDcPreChargeResponse()
        power_delivery_state = WaitForPowerDeliveryResponse()
        welding_detection_state = WaitForDcWeldingDetectionResponse()
        dc_charge_loop_state = WaitForDcChargeLoopResponse()
        session_stop_state = WaitForSessionStopResponse()
        states = [supported_app_protocol_state, session_setup_state, authorization_setup_state, authorization_state,
                  service_discovery_state, service_detail_state, service_selection_state,
                  charge_parameter_discovery_state, schedule_exchange_state, cable_check_state, pre_charge_state,
                  welding_detection_state, power_delivery_state, dc_charge_loop_state, session_stop_state]
        exitable_states = states[2:-3]

        # Transitions are defined like this: trigger, src, dst, conditions, unless, before, after, prepare
        transitions = [
                ["next_state", initial_state, supported_app_protocol_state],
                ["next_state", supported_app_protocol_state, session_setup_state],
                ["next_state", session_setup_state, authorization_setup_state],
                ["next_state", authorization_setup_state, authorization_state, None, 'stop_session'],
                ["next_state", authorization_state, service_discovery_state, None, 'stop_session'],
                ["next_state", service_discovery_state, service_detail_state, None, 'stop_session'],
                ["next_state", service_detail_state, service_selection_state, None, 'stop_session'],
                ["next_state", service_selection_state, charge_parameter_discovery_state, None, 'stop_session'],
                ["next_state", charge_parameter_discovery_state, schedule_exchange_state, None, 'stop_session'],
                ["next_state", schedule_exchange_state, cable_check_state, None, 'stop_session'],
                ["next_state", cable_check_state, pre_charge_state, None, 'stop_session'],
                ["next_state", pre_charge_state, pre_charge_state, 'processing'],
                ["next_state", pre_charge_state, power_delivery_state, None, ['processing', 'stop_session']],
                ["next_state", power_delivery_state, dc_charge_loop_state, 'charging'],
                ["next_state", dc_charge_loop_state, dc_charge_loop_state, 'charging'],
                ["next_state", dc_charge_loop_state, power_delivery_state, None, 'charging'],
                ["next_state", power_delivery_state, welding_detection_state, 'stop_session'],
                ["next_state", exitable_states, session_stop_state, 'stop_session']
            ]
        self.exitable_states = exitable_states
        super(EVSession, self).__init__(controller=controller, states=states, transitions=transitions,
                                        initial=supported_app_protocol_state)
        self.session_parameters = EVSessionParameters()
        # Creating a reference point for session parameters if access is needed
        for state in states:
            if state != initial_state:
                state.session_parameters = self.session_parameters
                state.controller = self.controller
        self.controller.stop = self.stop_loop # This line links controller.stop() method to self.stop_loop() method

    def processing(self):
        return self.session_parameters.processing

    def charging(self):
        return self.session_parameters.charging

    def stop_session(self):
        return self.session_parameters.stop_session

    def is_state_exitable(self, state):
        return state in self.exitable_states

    def stop_loop(self):
        self.session_parameters.stop_session = True
        self.session_parameters.charging = False
        logger.warning("Session stop has been requested.")
        return



@dataclass
class EVSessionParameters(SessionParameters):
    chosen_app_protocol = None
    evse_id = None
    selected_authorization_service = None
    selected_payment_option = None
    reaction = None
    charge_param_discovery_req = None
    charging: bool = False
    stop_session: bool = False
    processing: bool = False
    request_type: str = 'SAP'
