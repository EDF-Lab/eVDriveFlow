"""
.. module:: evse_dummy_controller
   :platform: Unix
   :synopsis: A module that implements the server's side controller for DC charging.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from typing import Optional, List
from shared.utils import rational_to_float, float_to_dc_rational, negative_dc_rational
from secc.evse_controller import IEVSEController, DcEVSEDataModel
from shared.global_values import V2G_CI_MSG_DC_NAMESPACE
from shared.xml_classes.app_protocol import AppProtocolType
from shared.xml_classes.common_messages import ServiceListType, ServiceType, AuthorizationType, \
    ServiceParameterListType, ParameterSetType, ParameterType, DynamicSeresControlModeType
from shared.xml_classes.dc import BptDcCpdresEnergyTransferMode, RationalNumberType as DcRationalNumberType, \
    BptDynamicDcClresControlMode
from dataclasses import dataclass, field
from shared.charge_controller_interface import ChargeControllerInterface
from shared.physical_interface import PhysicalInterface


class EVSEDummyController(IEVSEController):
    """Class that implements the DcBptDynamic EVSE controller.

    """
    def __init__(self):
        super(EVSEDummyController, self).__init__(EVSEEmulator(evsemaximum_voltage=DcRationalNumberType(2, 4),
                                                               evseminimum_voltage=DcRationalNumberType(0, 250),
                                                               evsemaximum_charge_power=DcRationalNumberType(3, 11),
                                                               evseminimum_charge_power=DcRationalNumberType(0, 500)),
                                                  PhysicalInterface("evse"))

    def set_machine(self):
        if self.virtual_mode:
            transitions = [
                ["plug", "A", "B", None, None, None, "set_b"],
                ["unplug", "B", "A", None, None, None, "set_a"],
                ["charge", "B", "C", None, None, None, "set_c"],
                ["unplug", "C", "A", None, None, None, "set_a"],
                ["stop_charge", "C", "B", None, None, None, "set_b"]
            ]
        else:
            self.state_machine = ChargeControllerInterface("169.254.43.20", 12500, "evse")
            transitions = [
                ["plug", "A", "B", "is_state_b", None, None, 'set_pwm'],
                ["unplug", "B", "A", "is_state_a"],
                ["charge", "B", "C", "is_state_c"],
                ["unplug", "C", "A", "is_state_a"],
                ["stop_charge", "C", "B", "is_state_b"]
            ]
        self.state_machine.add_transitions(transitions)


@dataclass
class EVSEEmulator(DcEVSEDataModel):
    departure_time: Optional[int] = 86400
    ev_departure_time: Optional[int] = 0
    _ev_departure_time: Optional[int] = 0
    minimum_soc: int = 0
    target_soc: int = 0
    _target_soc: Optional[int] = 0
    evsemaximum_charge_power: Optional[DcRationalNumberType] = None
    evseminimum_charge_power: Optional[DcRationalNumberType] = None
    evsemaximum_discharge_power: Optional[DcRationalNumberType] = None
    evseminimum_discharge_power: Optional[DcRationalNumberType] = None
    evsemaximum_charge_current: Optional[DcRationalNumberType] = None
    evseminimum_charge_current: Optional[DcRationalNumberType] = None
    evsemaximum_discharge_current: Optional[DcRationalNumberType] = None
    evseminimum_discharge_current: Optional[DcRationalNumberType] = None
    evsemaximum_voltage: Optional[DcRationalNumberType] = None
    evseminimum_voltage: Optional[DcRationalNumberType] = None
    evsepresent_current: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    evsepresent_power: Optional[DcRationalNumberType] = None  # This element is not specified in the standard, it is here
    # solely for the HMI.
    internal_resistance: Optional[float] = 100 * 10 ** -3
    energy_evolution = [0]
    power_evolution = [0]
    present_soc: int = 0
    _present_soc: int = field(init=False, repr=False)
    state: str = None
    _state: str = field(init=False, repr=False)
    battery_capacity: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _battery_capacity: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    consumed_energy: int = 0
    provided_energy: int = 0
    total_energy: int = 0
    evmaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evmaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    evmaximum_charge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evmaximum_charge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)

    def __post_init__(self):
        self.evseid = "ZZ000000"
        self.departure_time = 0
        self.supported_app_protocols = [AppProtocolType(protocol_namespace=V2G_CI_MSG_DC_NAMESPACE,
                                                        version_number_major=1, version_number_minor=0, priority=1)]
        self.authorization_services = [AuthorizationType.EIM]
        self.certificate_installation_service = False
        self.energy_transfer_service_list = ServiceListType([ServiceType(2, False), ServiceType(6, False)])
        self.service_renegotiation_supported = False
        self.services = {"6": ServiceParameterListType([ParameterSetType(1, [ParameterType(
            name="Connector", int_value=2), ParameterType(name="ControlMode", int_value=2), ParameterType(
            name="MobilityNeedsMode", int_value=2), ParameterType(name="Pricing", int_value=0), ParameterType(
            name="BPTChannel", int_value=1), ParameterType(name="GeneratorMode", int_value=1)])])}
        max_current = rational_to_float(self.evsemaximum_charge_power)
        max_current /= rational_to_float(self.evseminimum_voltage)
        self.evsemaximum_charge_current = self.evsemaximum_discharge_current = float_to_dc_rational(max_current)
        min_current = rational_to_float(self.evsemaximum_charge_power) / rational_to_float(self.evsemaximum_voltage)
        self.evseminimum_charge_current = self.evseminimum_discharge_current = float_to_dc_rational(min_current)
        self.evsepresent_voltage = self.evseminimum_voltage
        # self.evsepresent_current = DcRationalNumberType(0, 0) not useful when using ui
        self.evsemaximum_discharge_power = negative_dc_rational(self.evsemaximum_charge_power)
        self.evseminimum_discharge_power = negative_dc_rational(self.evseminimum_charge_power)
        self.evsemaximum_discharge_current = negative_dc_rational(self.evsemaximum_discharge_current)
        self.evseminimum_discharge_current = negative_dc_rational(self.evseminimum_discharge_current)

    def get_dynamic_seres_control_mode(self):
        """Builds message containing DynamicSeresControlModeType.

        :return: XML object.
        """
        response = DynamicSeresControlModeType()
        response.departure_time = self.departure_time
        return response

    def get_bpt_dc_cpdres_energy_transfer_mode(self):
        """Builds message containing BptDcCpdresEnergyTransferMode.

        :return: XML object.
        """
        response = BptDcCpdresEnergyTransferMode()
        response.evsemaximum_charge_current = self.evsemaximum_charge_current
        response.evseminimum_charge_current = self.evseminimum_charge_current
        response.evsemaximum_voltage = self.evsemaximum_voltage
        response.evseminimum_voltage = self.evseminimum_voltage
        response.evsemaximum_charge_power = self.evsemaximum_charge_power
        response.evseminimum_charge_power = self.evseminimum_charge_power
        response.evsemaximum_discharge_power = self.evsemaximum_discharge_power
        response.evseminimum_discharge_power = self.evseminimum_discharge_power
        response.evsemaximum_discharge_current = self.evsemaximum_discharge_current
        response.evseminimum_discharge_current = self.evseminimum_discharge_current
        return response

    def get_bpt_dynamic_dc_clres_control_mode(self):
        """Builds message containing BptDynamicDcClresControlMode.

        :return: XML object.
        """
        response = BptDynamicDcClresControlMode()
        response.departure_time = self.departure_time
        response.minimum_soc = self.minimum_soc
        response.target_soc = self.target_soc
        response.evsemaximum_charge_power = self.evsemaximum_charge_power
        response.evseminimum_charge_power = self.evseminimum_charge_power
        response.evsemaximum_charge_current = self.evsemaximum_charge_current
        response.evsemaximum_voltage = self.evsemaximum_voltage
        response.evseminimum_voltage = self.evseminimum_voltage
        response.evsemaximum_discharge_power = self.evsemaximum_discharge_power
        response.evseminimum_discharge_power = self.evseminimum_discharge_power
        response.evsemaximum_discharge_current = self.evsemaximum_discharge_current
        return response

    def update_charging_status(self, present_soc, battery_energy_capacity, power):
        """Updates data model by calculating values.

        :param present_soc: The present state of charge.
        :param battery_energy_capacity: The total battery capacity.
        :param power: The current power.
        :return:
        """
        self.present_soc = present_soc
        self.power_evolution.append(rational_to_float(power))
        battery_capacity = rational_to_float(battery_energy_capacity)
        self.energy_evolution.append(battery_capacity * present_soc / 100)
        energy_diff = self.energy_evolution[-1] - self.energy_evolution[-2]
        if energy_diff < 0:
            self.consumed_energy += abs(energy_diff)
        else:
            self.provided_energy += energy_diff
        self.total_energy = self.consumed_energy + self.provided_energy
        self.battery_capacity = battery_energy_capacity

    @property
    def present_soc(self):
        return self._present_soc

    @present_soc.setter
    def present_soc(self, value):
        self._present_soc = value
        self.notification_type = "15118"
        self.notify()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notification_type = "15118"
        self.notify()

    @property
    def battery_capacity(self):
        return self._battery_capacity

    @battery_capacity.setter
    def battery_capacity(self, value):
        self.notification_type = "ev_settings"
        self._battery_capacity = value
        self.notify()

    @property
    def ev_departure_time(self):
        return self._ev_departure_time

    @ev_departure_time.setter
    def ev_departure_time(self, value):
        self._ev_departure_time = value
        self.departure_time = value
        self.notification_type = "timer"
        self.notify()

    @property
    def target_soc(self):
        return self._target_soc

    @target_soc.setter
    def target_soc(self, value):
        self._target_soc = value
        self.notification_type = "target_soc"
        self.notify()

    @property
    def evmaximum_charge_power(self):
        return self._evmaximum_charge_power

    @evmaximum_charge_power.setter
    def evmaximum_charge_power(self, value):
        self._evmaximum_charge_power = value
        self.notification_type = "ev_settings"
        self.notify()

    @property
    def evmaximum_discharge_power(self):
        return self._evmaximum_discharge_power

    @evmaximum_discharge_power.setter
    def evmaximum_discharge_power(self, value):
        self._evmaximum_discharge_power = value
        self.notification_type = "ev_settings"
        self.notify()
