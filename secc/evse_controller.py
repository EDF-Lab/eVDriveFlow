"""
.. module:: evse_controller
   :platform: Unix
   :synopsis: A module that implements the server's side controller.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from dataclasses import dataclass, field
from typing import Optional, List
from shared.xml_classes.app_protocol import AppProtocolType
from shared.xml_classes.common_messages import AuthorizationType, ServiceListType, PnCAsresAuthorizationModeType, \
    ProcessingType, ServiceParameterListType, EvsestatusType
from shared.xml_classes.dc import BptDcCpdresEnergyTransferMode, DcCpdresEnergyTransferMode, ProcessingType as \
    DcProcessingType, RationalNumberType as DcRationalNumberType, BptDynamicDcClresControlMode, \
    DynamicDcClresControlMode, BptScheduledDcClresControlMode, ScheduledDcClresControlMode, ClresControlMode as \
    DcClresControlMode
from configparser import ConfigParser
from shared.controller import ControllerInterface
from shared.gui import GUI


@dataclass
class EVSEDataModel:
    """Data model containing anything related to the EVSE.

    """
    _observers: List[GUI] = field(default_factory=list)
    notification_type: str = None
    # ProcessSupportedAppProtocol
    supported_app_protocols: List[AppProtocolType] = None
    # ProcessSessionSetup
    evseid: Optional[str] = None
    # ProcessAuthorizationSetup
    authorization_services: List[AuthorizationType] = None
    certificate_installation_service: Optional[bool] = None
    # ProcessAuthorizationSetup
    evseprocessing: Optional[ProcessingType] = None
    # ProcessServiceDiscovery
    service_renegotiation_supported: Optional[bool] = None
    energy_transfer_service_list: Optional[ServiceListType] = None
    vaslist: Optional[ServiceListType] = None
    # ProcessServiceDetail
    service_id: Optional[int] = None
    services: List[ServiceParameterListType] = None
    # ProcessPowerDelivery
    evsestatus: Optional[EvsestatusType] = None

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


@dataclass
class DcEVSEDataModel(EVSEDataModel):
    # ProcessDcChargeParameterDiscovery
    bpt_dc_cpdres_energy_transfer_mode: Optional[BptDcCpdresEnergyTransferMode] = None
    dc_cpdres_energy_transfer_mode: Optional[DcCpdresEnergyTransferMode] = None
    # ProcessDcCableCheck
    dc_evseprocessing: Optional[DcProcessingType] = None
    # ProcessDcPreCharge
    evsepresent_voltage: Optional[DcRationalNumberType] = None
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


class IEVSEController(ControllerInterface):
    def get_config(self):
        config = ConfigParser()
        config.read("evse_config.ini")
        return config


class IDcEVSEController(IEVSEController):
    charge_ev: bool = False

    def __init__(self):
        super(IDcEVSEController, self).__init__(DcEVSEDataModel())
