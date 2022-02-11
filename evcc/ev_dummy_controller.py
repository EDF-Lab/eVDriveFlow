"""
.. module:: ev_dummy_controller
   :platform: Unix
   :synopsis: A module that implements the client's side controller for DC charging.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from typing import Optional
from evcc.ev_controller import IEVController, DcEVDataModel
import numpy as np
from shared.global_values import V2G_CI_MSG_DC_NAMESPACE
from shared.xml_classes.app_protocol import AppProtocolType
from shared.xml_classes.common_messages import ServiceIdlistType, AuthorizationType, DynamicSereqControlModeType
from shared.xml_classes.dc import BptDcCpdreqEnergyTransferMode, RationalNumberType as DcRationalNumberType, \
    BptDynamicDcClreqControlMode
from shared.xml_classes.common_messages import RationalNumberType
from dataclasses import dataclass, field
from shared.utils import rational_to_float, float_to_dc_rational
from shared.charge_controller_interface import ChargeControllerInterface


class EVDummyController(IEVController):
    """Class that implements the DcBptDynamic EV controller.

    """
    def __init__(self):
        super(EVDummyController, self).__init__(EVEmulator(battery_capacity=DcRationalNumberType(3, 67),
                                                           evmaximum_voltage=DcRationalNumberType(0, 360),
                                                           evminimum_voltage=DcRationalNumberType(0, 310)))

    def set_machine(self):
        # Transitions syntax: 
        # [ Trigger, Source, Destination, Conditions, Unless, Before, After, Prepare]
        if self.virtual_mode:
            transitions = [
                ["plug", "A", "B", None, None, None, ["unset_pwm", "set_b"]],
                ["unplug", "B", "A", None, None, None, "set_a"],
                ["charge", "B", "C", "pwm_on", None, None, "set_c"],
                ["unplug", "C", "A", None, None, None, "set_a"],
                ["stop_charge", "C", "B", None, None, None, "set_b"]
            ]
        else:
            self.state_machine = ChargeControllerInterface("169.254.43.3", 12500)
            transitions = [
                #["plug", "A", "B", "is_state_a", None, None, "set_b"],
                ["plug", "E", "B", "is_state_b", None, None, "set_b"],
                ["unplug", "B", "A", "is_state_b"],
                ["charge", "B", "C", "is_state_b", None, None, "set_c"],
                ["unplug", "C", "A", "is_state_c"],
                ["stop_charge", "C", "B", "is_state_c", None, None, "set_b"]
            ]
        self.state_machine.add_transitions(transitions)


@dataclass
class EVEmulator(DcEVDataModel):
    timestamp: float = 0
    timestep: float = 0
    minimum_soc: int = 0
    maximum_soc: int = 100
    departure_time: int = 0
    _departure_time: int = 0
    battery_capacity: DcRationalNumberType = None
    target_soc: int = 0
    _target_soc: int = 0
    present_soc: int = 0
    evmaximum_voltage: DcRationalNumberType = None
    evminimum_voltage: DcRationalNumberType = None
    evpresent_voltage: DcRationalNumberType = None
    current_energy: Optional[float] = None
    soc: np.array = None
    max_charge_power: np.array = None
    max_discharge_power: np.array = None
    # figure details
    energy_evolution = [0]
    soc_evolution = [present_soc]
    power_evolution = [0]
    elapsed_time: float = 0
    present_soc: int = 0
    _present_soc: int = field(init=False, repr=False)
    state: str = None
    _state: str = field(init=False, repr=False)
    _battery_capacity: Optional[DcRationalNumberType] = field(init=False, repr=False)
    consumed_energy: int = 0
    provided_energy: int = 0
    total_energy: int = 0
    evsemaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evsemaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    evsemaximum_charge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evsemaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    evmaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evmaximum_discharge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    evmaximum_charge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)
    _evmaximum_charge_power: Optional[DcRationalNumberType] = DcRationalNumberType(0, 0)

    def __post_init__(self):
        self.supported_app_protocols = [AppProtocolType(protocol_namespace=V2G_CI_MSG_DC_NAMESPACE,
                                                        version_number_major=2, version_number_minor=0,
                                                        schema_id=1, priority=1)]
        self.evccid = "FR8VAA0000453C4D58Y2"
        self.authorization_services = [AuthorizationType.EIM]
        self.supported_service_ids = ServiceIdlistType([2, 6])
        self.present_soc = 0
        self.current_energy = 0
        self.evpresent_voltage = DcRationalNumberType(0, 0)
        self.soc = np.linspace(0, 100, 21)
        self.max_charge_power = 1000 * np.array([49, 49, 49, 49, 49, 49, 49, 49, 48, 46, 44, 42, 40, 37, 34, 31, 27, 23,
                                                 19, 14, 0])
        self.max_discharge_power = - np.flip(self.max_charge_power)

    def get_max_charge_parameters(self) -> (DcRationalNumberType, DcRationalNumberType):
        """Gets max charge power and max current from a vehicle's charging data.

        :return: (DcRationalNumberType, DcRationalNumberType) -- max charge power and max current.
        """
        max_charge_pow = np.interp(self.present_soc, self.soc, self.max_charge_power)
        if self.present_soc < 99:
            max_current = max_charge_pow / battery_voltage_profile(self.present_soc)
        else:
            max_current = 0
        return float_to_dc_rational(max_charge_pow), float_to_dc_rational(max_current)

    def get_min_charge_parameters(self) -> (DcRationalNumberType, DcRationalNumberType):
        """Gets min charge power and min current from a vehicle's charging data.

        :return: (DcRationalNumberType, DcRationalNumberType) -- min charge power and min current.
        """
        min_charge_power = 0.005 * self.max_charge_power[np.argmax(self.max_charge_power)]
        min_charge_current = min_charge_power / rational_to_float(self.evmaximum_voltage)
        return float_to_dc_rational(min_charge_power), float_to_dc_rational(min_charge_current)

    def get_max_discharge_parameters(self) -> (DcRationalNumberType, DcRationalNumberType):
        """Gets max discharge power and max discharge current from a vehicle's charging data.

        :return: (DcRationalNumberType, DcRationalNumberType) -- max discharge power and max discharge current.
        """
        max_discharge_pow = np.interp(self.present_soc, self.soc, self.max_discharge_power)
        if self.present_soc <= 1:
            max_discharge_current = 0
        else:
            max_discharge_current = max_discharge_pow / battery_voltage_profile(self.present_soc)
        return float_to_dc_rational(max_discharge_pow), float_to_dc_rational(max_discharge_current)

    def get_min_discharge_parameters(self) -> (DcRationalNumberType, DcRationalNumberType):
        """Gets min discharge power and min discharge current from a vehicle's charging data.

        :return: (DcRationalNumberType, DcRationalNumberType) -- min discharge power and min discharge current.
        """
        min_discharge_pow = np.interp(self.present_soc, self.soc, self.max_discharge_power)
        min_discharge_current = min_discharge_pow / rational_to_float(self.evmaximum_voltage)
        return float_to_dc_rational(min_discharge_pow), float_to_dc_rational(min_discharge_current)

    def get_voltage_limits(self) -> (DcRationalNumberType, DcRationalNumberType):
        """Returns the EV voltage limits.

        :return: (DcRationalNumberType, DcRationalNumberType) -- max and min limits.
        """
        return self.evmaximum_voltage, self.evminimum_voltage

    def get_current_energy(self) -> float:
        """Gets the current energy value.

        :return: float - current energy.
        """
        return self.present_soc / 100 * rational_to_float(self.battery_capacity)

    def get_target_energy(self) -> float:
        """Gets target energy.

        :return: float - target energy.
        """
        return self.target_soc * rational_to_float(self.battery_capacity) - self.current_energy

    def get_max_energy(self) -> float:
        """Gets max energy.

        :return: float - max energy.
        """
        return rational_to_float(self.battery_capacity) - self.current_energy

    def get_min_energy(self) -> float:
        """Gets min energy.

        :return: float - min energy.
        """
        return self.minimum_soc * rational_to_float(self.battery_capacity) - self.current_energy

    def update_charging_status(self, present_current, present_voltage, time_step):
        """Updates the battery values.

        :param present_current: The present current.
        :param present_voltage: The present voltage.
        :param time_step: The time spent between two ticks of charge.
        :return:
        """
        self.soc_evolution.append(self.present_soc)
        self.energy_evolution.append(self.current_energy)
        self.evpresent_voltage = float_to_dc_rational(battery_voltage_profile(self.present_soc))
        present_power = rational_to_float(present_current) * rational_to_float(present_voltage)
        # TODO: the power test limit should be located in states process_payload
        if present_power < 0:
            evse_max_power = rational_to_float(self.evsemaximum_discharge_power)
            ev_max_power = rational_to_float(self.evmaximum_discharge_power)
            present_power = max(evse_max_power, ev_max_power, present_power)
        else:
            evse_max_power = rational_to_float(self.evsemaximum_charge_power)
            ev_max_power = rational_to_float(self.evmaximum_charge_power)
            present_power = min(evse_max_power, ev_max_power, present_power)
        self.current_energy = int(self.current_energy + present_power * time_step / 3600 * 100)
        # TODO: time mutiplied by 100 (to be removed)
        self.present_soc = int(self.current_energy * 100 / rational_to_float(self.battery_capacity))
        self.power_evolution.append(present_power)
        self.elapsed_time += time_step
        energy_diff = self.energy_evolution[-1] - self.energy_evolution[-2]
        self.evmaximum_discharge_power = self.get_max_discharge_parameters()[0]
        self.evmaximum_charge_power = self.get_max_charge_parameters()[0]
        if energy_diff < 0:
            self.provided_energy += abs(energy_diff)
        else:
            self.consumed_energy += abs(energy_diff)
        self.total_energy = self.consumed_energy + self.provided_energy

    def get_dynamic_sereq_control_mode(self) -> DynamicSereqControlModeType:
        """Returns DynamicSereqControlModeType request.

        :return: DynamicSereqControlModeType -- the message.
        """
        request = DynamicSereqControlModeType()
        request.departure_time = self.departure_time
        request.minimum_soc = self.minimum_soc
        request.target_soc = self.target_soc
        request.evtarget_energy_request = RationalNumberType(3, 67)
        request.evmaximum_energy_request = RationalNumberType(3, 67)
        request.evminimum_energy_request = RationalNumberType(0, 0)
        return request

    def get_bpt_dc_cpdreq_energy_transfer_mode(self) -> BptDcCpdreqEnergyTransferMode:
        """Returns BptDcCpdreqEnergyTransferMode request.

        :return: BptDcCpdreqEnergyTransferMode -- the request.
        """
        request = BptDcCpdreqEnergyTransferMode()
        request.evmaximum_charge_power, request.evmaximum_charge_current = self.get_max_charge_parameters()
        request.evminimum_charge_power, request.evminimum_charge_current = self.get_min_charge_parameters()
        request.evmaximum_voltage = self.evmaximum_voltage
        request.evminimum_voltage = self.evminimum_voltage
        request.target_soc = self.target_soc
        request.evmaximum_discharge_power, request.evmaximum_discharge_current = self.get_max_discharge_parameters()
        request.evminimum_discharge_power, request.evminimum_discharge_current = self.get_min_discharge_parameters()
        return request

    def get_bpt_dynamic_dc_clreq_control_mode(self) -> BptDynamicDcClreqControlMode:
        """Returns BptDynamicDcClreqControlMode request.

        :return: BptDynamicDcClreqControlMode -- the request
        """
        request = BptDynamicDcClreqControlMode()
        request.departure_time = self.departure_time
        request.evtarget_energy_request = float_to_dc_rational(self.get_target_energy())
        request.evmaximum_energy_request = float_to_dc_rational(self.get_max_energy())
        request.evminimum_energy_request = float_to_dc_rational(self.get_min_energy())
        request.evmaximum_charge_power, request.evmaximum_charge_current = self.get_max_charge_parameters()
        request.evminimum_charge_power, request.evminimum_charge_current = self.get_min_charge_parameters()
        request.evmaximum_voltage = self.evmaximum_voltage
        request.evminimum_voltage = self.evminimum_voltage
        request.evmaximum_discharge_power, request.evmaximum_discharge_current = self.get_max_discharge_parameters()
        request.evminimum_discharge_power, request.evminimum_discharge_current = self.get_min_discharge_parameters()
        return request

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
    def departure_time(self):
        return self._departure_time

    @departure_time.setter
    def departure_time(self, value):
        self._departure_time = value
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
    def evsemaximum_charge_power(self):
        return self._evsemaximum_charge_power

    @evsemaximum_charge_power.setter
    def evsemaximum_charge_power(self, value):
        self._evsemaximum_charge_power = value
        self.notification_type = "ev_settings"
        self.notify()

    @property
    def evsemaximum_discharge_power(self):
        return self._evsemaximum_discharge_power

    @evsemaximum_discharge_power.setter
    def evsemaximum_discharge_power(self, value):
        self._evsemaximum_discharge_power = value
        self.notification_type = "ev_settings"
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


def battery_voltage_profile(soc) -> float:
    """The battery profile.

    :param soc: State of charge
    :return: float -- the present voltage.
    """
    if 0 <= soc <= 75:
        return 50 * soc / 75 + 310
    return 360

