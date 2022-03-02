"""
.. module:: evse_session
   :platform: Unix
   :synopsis: A module that implements the server's side communication session.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from typing import Optional, List
from secc.states.process_authorization_request import ProcessAuthorizationRequest
from secc.states.process_authorization_setup_request import ProcessAuthorizationSetupRequest
from secc.states.process_dc_cable_check_request import ProcessDcCableCheckRequest
from secc.states.process_dc_charge_parameter_discovery_request import ProcessDcChargeParameterDiscoveryRequest
from secc.states.process_dc_charge_loop_request import ProcessDcChargeLoopRequest
from secc.states.process_power_delivery_request import ProcessPowerDeliveryRequest
from secc.states.process_dc_pre_charge_request import ProcessDcPreChargeRequest
from secc.states.process_schedule_exchange_request import ProcessScheduleExchangeRequest
from secc.states.process_service_detail_request import ProcessServiceDetailRequest
from secc.states.process_service_discovery_request import ProcessServiceDiscoveryRequest
from secc.states.process_service_selection_request import ProcessServiceSelectionRequest
from secc.states.process_session_setup_request import ProcessSessionSetupRequest
from secc.states.process_session_stop_request import ProcessSessionStopRequest
from secc.states.process_supported_app_protocol_request import ProcessSupportedAppProtocolRequest
from secc.states.process_dc_welding_detection_request import ProcessDcWeldingDetectionRequest
from shared.session import CommunicationSession
import secrets
from dataclasses import dataclass
from shared.session import SessionParameters
from shared.xml_classes.common_messages import AuthorizationType, ServiceListType, PnCAsresAuthorizationModeType, \
    ProcessingType, ServiceParameterListType, EvsestatusType
from shared.xml_classes.dc import BptDcCpdresEnergyTransferMode, DcCpdresEnergyTransferMode, ProcessingType as \
    DcProcessingType, RationalNumberType as DcRationalNumberType, BptDynamicDcClresControlMode, \
    DynamicDcClresControlMode, BptScheduledDcClresControlMode, ScheduledDcClresControlMode, ClresControlMode as \
    DcClresControlMode


class EVSESession(CommunicationSession):
    """Represents a EVSE side communication session. Built with a state machine.

    """
    def __init__(self, controller):
        """Basic constructor.

        :param controller: The controller that will handle the data.
        """
        # Defining the different states
        initial_state = "initial_state"
        supported_app_protocol_state = ProcessSupportedAppProtocolRequest()
        session_setup_state = ProcessSessionSetupRequest()
        authorization_setup_state = ProcessAuthorizationSetupRequest()
        authorization_state = ProcessAuthorizationRequest()
        service_discovery_state = ProcessServiceDiscoveryRequest()
        service_detail_state = ProcessServiceDetailRequest()
        service_selection_state = ProcessServiceSelectionRequest()
        charge_parameter_discovery_state = ProcessDcChargeParameterDiscoveryRequest()
        schedule_exchange_state = ProcessScheduleExchangeRequest()
        cable_check_state = ProcessDcCableCheckRequest()
        pre_charge_state = ProcessDcPreChargeRequest()
        power_delivery_state = ProcessPowerDeliveryRequest()
        welding_detection_state = ProcessDcWeldingDetectionRequest()
        dc_charge_loop_state = ProcessDcChargeLoopRequest()
        session_stop_state = ProcessSessionStopRequest()
        states = [supported_app_protocol_state, session_setup_state, authorization_setup_state, authorization_state,
                  service_discovery_state, service_detail_state, service_selection_state,
                  charge_parameter_discovery_state, schedule_exchange_state, cable_check_state, pre_charge_state,
                  welding_detection_state, power_delivery_state, dc_charge_loop_state, session_stop_state]
        exitable_states = states[2:-3]
        # Transitions are defined like this: trigger, src, dst, conditions, unless, before, after, prepare
        transitions = [
            ["next_message", initial_state, supported_app_protocol_state],
            ["next_message", supported_app_protocol_state, session_setup_state],
            ["next_message", session_setup_state, authorization_setup_state],
            ["next_message", authorization_setup_state, authorization_state],
            ["next_message", authorization_state, service_discovery_state],
            ["next_message", service_discovery_state, service_detail_state],
            ["next_message", service_detail_state, service_selection_state],
            ["next_message", service_selection_state, charge_parameter_discovery_state],
            ["next_message", charge_parameter_discovery_state, schedule_exchange_state],
            ["next_message", schedule_exchange_state, cable_check_state],
            ["next_message", cable_check_state, pre_charge_state],
            ["next_message", pre_charge_state, power_delivery_state],
            ["next_message", power_delivery_state, welding_detection_state],
            ["next_message", power_delivery_state, dc_charge_loop_state],
            ["next_message", dc_charge_loop_state, dc_charge_loop_state],
            ["next_message", dc_charge_loop_state, power_delivery_state],
            ["next_message", exitable_states, session_stop_state]
        ]
        super(EVSESession, self).__init__(controller=controller, states=states, transitions=transitions,
                                          initial=initial_state)
        self.session_parameters = EVSESessionParameters()
        # Creating a reference point for session parameters and controller if access is needed
        for state in states:
            if state != initial_state:
                state.session_parameters = self.session_parameters
                state.controller = self.controller
        self.session_parameters.session_id = self.generate_random_session_id()

    @staticmethod
    def generate_random_session_id() -> str:
        """
        Generates a random 8-length int number. See [V2G20-2621] for more detail. Might have security issues.

        :return: str -- the resulting id.
        """
        return str(secrets.randbelow(100000000)).zfill(8).encode('ascii')


@dataclass
class EVSESessionParameters(SessionParameters):
    # ProcessSessionSetup
    evseid: Optional[str] = None
    # ProcessAuthorizationSetup
    authorization_services: List[AuthorizationType] = None
    certificate_installation_service: Optional[bool] = None
    eim_asres_authorization_mode: Optional[object] = None
    pn_c_asres_authorization_mode: Optional[PnCAsresAuthorizationModeType] = None
    # ProcessAuthorizationSetup
    evseprocessing: Optional[ProcessingType] = None
    # ProcessServiceDiscovery
    service_renegotiation_supported: Optional[bool] = None
    energy_transfer_service_list: Optional[ServiceListType] = None
    vaslist: Optional[ServiceListType] = None
    # ProcessServiceDetail
    service_id: Optional[int] = None
    service_parameter_list: Optional[ServiceParameterListType] = None
    # ProcessDcChargeParameterDiscovery
    bpt_dc_cpdres_energy_transfer_mode: Optional[BptDcCpdresEnergyTransferMode] = None
    dc_cpdres_energy_transfer_mode: Optional[DcCpdresEnergyTransferMode] = None
    # ProcessDcCableCheck
    dc_evseprocessing: Optional[DcProcessingType] = None
    # ProcessDcPreCharge
    evsepresent_voltage: Optional[DcRationalNumberType] = None
    # ProcessPowerDelivery
    evsestatus: Optional[EvsestatusType] = None
    # ProcessDcChargeLoop
    evsepresent_current: Optional[DcRationalNumberType] = None
    evsepower_limit_achieved: Optional[bool] = None
    evsecurrent_limit_achieved: Optional[bool] = None
    evsevoltage_limit_achieved: Optional[bool] = None
    bpt_dynamic_dc_clres_control_mode: Optional[BptDynamicDcClresControlMode] = None
    dynamic_dc_clres_control_mode: Optional[DynamicDcClresControlMode] = None
    bpt_scheduled_dc_clres_control_mode: Optional[BptScheduledDcClresControlMode] = None
    scheduled_dc_clres_control_mode: Optional[ScheduledDcClresControlMode] = None
    clres_control_mode: Optional[DcClresControlMode] = None
