"""
.. module:: ev_controller
   :platform: Unix
   :synopsis: A module that implements the client's side controller.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.controller import ControllerInterface
from typing import Optional, List
from shared.xml_classes.app_protocol import AppProtocolType
from shared.xml_classes.common_messages import AuthorizationType, PnCAreqAuthorizationModeType, ServiceIdlistType, \
    SelectedServiceType, SelectedServiceListType, ChargeProgressType, EvpowerProfileType, ChannelSelectionType, \
    ProcessingType
from shared.xml_classes.dc import BptDcCpdreqEnergyTransferMode, DcCpdreqEnergyTransferMode, ProcessingType as \
    DcProcessingType, RationalNumberType as DcRationalNumberType, BptDynamicDcClreqControlMode, \
    DynamicDcClreqControlMode, BptScheduledDcClreqControlMode, ScheduledDcClreqControlMode, ClreqControlMode as \
    DcClreqControlMode
from dataclasses import dataclass, field
from configparser import ConfigParser
from shared.gui import GUI


@dataclass
class EVDataModel:
    """Data model containing anything related to the EV.

    """
    _observers: List[GUI] = field(default_factory=list)
    notification_type: str = None
    # SupportedAppProtocol
    supported_app_protocols: List[AppProtocolType] = None
    # SessionSetup
    evccid: Optional[bytes] = None
    # Authorization
    authorization_services: List[AuthorizationType] = None
    selected_authorization_service: Optional[AuthorizationType] = None
    eim_areq_authorization_mode: Optional[object] = None
    pn_c_areq_authorization_mode: Optional[PnCAreqAuthorizationModeType] = None
    # ServiceDiscovery
    supported_service_ids: Optional[ServiceIdlistType] = None
    # ServiceDetail
    service_id: Optional[int] = None
    # ServiceSelection
    selected_energy_transfer_service: Optional[SelectedServiceType] = None
    selected_vaslist: Optional[SelectedServiceListType] = None
    # PowerDelivery
    evprocessing: Optional[ProcessingType] = None
    charge_progress: Optional[ChargeProgressType] = None
    evpower_profile: Optional[EvpowerProfileType] = None
    bpt_channel_selection: Optional[ChannelSelectionType] = None

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


@dataclass
class DcEVDataModel(EVDataModel):
    # DcChargeParameterDiscovery
    bpt_dc_cpdreq_energy_transfer_mode: Optional[BptDcCpdreqEnergyTransferMode] = None
    dc_cpdreq_energy_transfer_mode: Optional[DcCpdreqEnergyTransferMode] = None
    # DcPreCharge
    evprocessing: Optional[DcProcessingType] = None
    evtarget_voltage: Optional[DcRationalNumberType] = None
    # DcChargeLoop
    evpresent_voltage: Optional[DcRationalNumberType] = None
    bpt_dynamic_dc_clreq_control_mode: Optional[BptDynamicDcClreqControlMode] = None
    dynamic_dc_clreq_control_mode: Optional[DynamicDcClreqControlMode] = None
    bpt_scheduled_dc_clreq_control_mode: Optional[BptScheduledDcClreqControlMode] = None
    scheduled_dc_clreq_control_mode: Optional[ScheduledDcClreqControlMode] = None
    clreq_control_mode: Optional[DcClreqControlMode] = None


@dataclass
class IEVController(ControllerInterface):
    udp_port: int = None

    def get_config(self):
        config = ConfigParser()
        config.read("ev_config.ini")
        return config

    def set_network_parameters(self):
        config = self.get_config()["NETWORK"]
        self.interface = config["interface"]
        self.udp_port = config.getint("udp_port")
        self.tcp_port = config.getint("tcp_port")


class IDcEVController(IEVController):
    def __init__(self):
        super(IDcEVController, self).__init__(DcEVDataModel())
