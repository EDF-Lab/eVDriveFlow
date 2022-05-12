from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from shared.xml_classes.common_messages.v2_g_ci_common_types import (
    EvsestatusType,
    ListOfRootCertificateIdsType,
    MeterInfoType,
    RationalNumberType,
    ReceiptType,
    V2GrequestType,
    V2GresponseType,
    ProcessingType,
)

__NAMESPACE__ = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class DynamicEvpptcontrolModeType:
    class Meta:
        name = "Dynamic_EVPPTControlModeType"


@dataclass
class DynamicSmdtcontrolModeType:
    class Meta:
        name = "Dynamic_SMDTControlModeType"


@dataclass
class EimAreqAuthorizationModeType:
    class Meta:
        name = "EIM_AReqAuthorizationModeType"


@dataclass
class EimAsresAuthorizationModeType:
    class Meta:
        name = "EIM_ASResAuthorizationModeType"


@dataclass
class EmaidlistType:
    class Meta:
        name = "EMAIDListType"

    emaid: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EMAID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 8,
            "max_length": 255,
        }
    )


@dataclass
class PriceLevelScheduleEntryType:
    duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    price_level: Optional[int] = field(
        default=None,
        metadata={
            "name": "PriceLevel",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class PriceScheduleType:
    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    price_schedule_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "PriceScheduleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )
    price_schedule_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "PriceScheduleDescription",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 160,
        }
    )


@dataclass
class ScheduledSmdtcontrolModeType:
    class Meta:
        name = "Scheduled_SMDTControlModeType"

    selected_schedule_tuple_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "SelectedScheduleTupleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )


@dataclass
class SelectedServiceType:
    service_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ServiceID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    parameter_set_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ParameterSetID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class ServiceIdlistType:
    class Meta:
        name = "ServiceIDListType"

    service_id: List[int] = field(
        default_factory=list,
        metadata={
            "name": "ServiceID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 16,
        }
    )


@dataclass
class ServiceType:
    service_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ServiceID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    free_service: Optional[bool] = field(
        default=None,
        metadata={
            "name": "FreeService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class SubCertificatesType:
    certificate: List[bytes] = field(
        default_factory=list,
        metadata={
            "name": "Certificate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 3,
            "max_length": 1600,
            "format": "base64",
        }
    )


@dataclass
class SupportedProvidersListType:
    provider_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "ProviderID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 128,
            "max_length": 80,
        }
    )


@dataclass
class TargetPositionType:
    target_offset_x: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetOffsetX",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    target_offset_y: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetOffsetY",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


class AuthorizationType(Enum):
    EIM = "EIM"
    PN_C = "PnC"


class ChannelSelectionType(Enum):
    CHARGE = "Charge"
    DISCHARGE = "Discharge"


class ChargeProgressType(Enum):
    START = "Start"
    STOP = "Stop"
    STANDBY = "Standby"
    SCHEDULE_RENEGOTIATION = "ScheduleRenegotiation"


class ChargingSessionType(Enum):
    PAUSE = "Pause"
    TERMINATE = "Terminate"
    SERVICE_RENEGOTIATION = "ServiceRenegotiation"


class EcdhCurveType(Enum):
    SECP521 = "SECP521"
    X448 = "X448"


class EvCheckInStatusType(Enum):
    CHECK_IN = "CheckIn"
    PROCESSING = "Processing"
    COMPLETED = "Completed"


class EvCheckOutStatusType(Enum):
    CHECK_OUT = "CheckOut"
    PROCESSING = "Processing"
    COMPLETED = "Completed"


class EvseCheckOutStatusType(Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"


class ParkingMethodType(Enum):
    AUTO_PARKING = "AutoParking"
    MVGUIDE_MANUAL = "MVGuideManual"
    MANUAL = "Manual"


class PowerToleranceAcceptanceType(Enum):
    POWER_TOLERANCE_NOT_CONFIRMED = "PowerToleranceNotConfirmed"
    POWER_TOLERANCE_CONFIRMED = "PowerToleranceConfirmed"


@dataclass
class AdditionalServiceType:
    service_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServiceName",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 80,
        }
    )
    service_fee: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "ServiceFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class AuthorizationResType(V2GresponseType):
    evseprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVSEProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class AuthorizationSetupReqType(V2GrequestType):
    pass


@dataclass
class CertificateChainType:
    certificate: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "Certificate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 1600,
            "format": "base64",
        }
    )
    sub_certificates: Optional[SubCertificatesType] = field(
        default=None,
        metadata={
            "name": "SubCertificates",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ContractCertificateChainType:
    certificate: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "Certificate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 1600,
            "format": "base64",
        }
    )
    sub_certificates: Optional[SubCertificatesType] = field(
        default=None,
        metadata={
            "name": "SubCertificates",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class DynamicSereqControlModeType:
    class Meta:
        name = "Dynamic_SEReqControlModeType"

    departure_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "DepartureTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    minimum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "MinimumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    evtarget_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evmaximum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evminimum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evmaximum_v2_xenergy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumV2XEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evminimum_v2_xenergy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumV2XEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class EvpowerScheduleEntryType:
    class Meta:
        name = "EVPowerScheduleEntryType"

    duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Power",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class EvpriceRuleType:
    class Meta:
        name = "EVPriceRuleType"

    energy_fee: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EnergyFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    power_range_start: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "PowerRangeStart",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class MeteringConfirmationResType(V2GresponseType):
    pass


@dataclass
class OverstayRuleType:
    overstay_rule_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "OverstayRuleDescription",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 160,
        }
    )
    start_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "StartTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    overstay_fee: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "OverstayFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    overstay_fee_period: Optional[int] = field(
        default=None,
        metadata={
            "name": "OverstayFeePeriod",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class ParameterType:
    bool_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "boolValue",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    byte_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "byteValue",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    short_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "shortValue",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    int_value: Optional[int] = field(
        default=None,
        metadata={
            "name": "intValue",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    rational_number: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "rationalNumber",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    finite_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "finiteString",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 80,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 80,
        }
    )


@dataclass
class PnCAsresAuthorizationModeType:
    class Meta:
        name = "PnC_ASResAuthorizationModeType"

    gen_challenge: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "GenChallenge",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "length": 16,
            "format": "base64",
        }
    )
    supported_providers: Optional[SupportedProvidersListType] = field(
        default=None,
        metadata={
            "name": "SupportedProviders",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class PowerDeliveryResType(V2GresponseType):
    evsestatus: Optional[EvsestatusType] = field(
        default=None,
        metadata={
            "name": "EVSEStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class PowerScheduleEntryType:
    duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Power",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    power_l2: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Power_L2",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    power_l3: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Power_L3",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class PriceLevelScheduleEntryListType:
    price_level_schedule_entry: List[PriceLevelScheduleEntryType] = field(
        default_factory=list,
        metadata={
            "name": "PriceLevelScheduleEntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 1024,
        }
    )


@dataclass
class PriceRuleType:
    energy_fee: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EnergyFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    parking_fee: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "ParkingFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    parking_fee_period: Optional[int] = field(
        default=None,
        metadata={
            "name": "ParkingFeePeriod",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    carbon_dioxide_emission: Optional[int] = field(
        default=None,
        metadata={
            "name": "CarbonDioxideEmission",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    renewable_generation_percentage: Optional[int] = field(
        default=None,
        metadata={
            "name": "RenewableGenerationPercentage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    power_range_start: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "PowerRangeStart",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class ScheduledEvpptcontrolModeType:
    class Meta:
        name = "Scheduled_EVPPTControlModeType"

    selected_schedule_tuple_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "SelectedScheduleTupleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )
    power_tolerance_acceptance: Optional[PowerToleranceAcceptanceType] = field(
        default=None,
        metadata={
            "name": "PowerToleranceAcceptance",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class SelectedServiceListType:
    selected_service: List[SelectedServiceType] = field(
        default_factory=list,
        metadata={
            "name": "SelectedService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 16,
        }
    )


@dataclass
class ServiceDetailReqType(V2GrequestType):
    service_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ServiceID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class ServiceDiscoveryReqType(V2GrequestType):
    supported_service_ids: Optional[ServiceIdlistType] = field(
        default=None,
        metadata={
            "name": "SupportedServiceIDs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ServiceListType:
    service: List[ServiceType] = field(
        default_factory=list,
        metadata={
            "name": "Service",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 8,
        }
    )


@dataclass
class ServiceSelectionResType(V2GresponseType):
    pass


@dataclass
class SessionSetupReqType(V2GrequestType):
    evccid: Optional[str] = field(
        default=None,
        metadata={
            "name": "EVCCID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 255,
        }
    )


@dataclass
class SessionSetupResType(V2GresponseType):
    evseid: Optional[str] = field(
        default=None,
        metadata={
            "name": "EVSEID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 255,
        }
    )


@dataclass
class SessionStopReqType(V2GrequestType):
    charging_session: Optional[ChargingSessionType] = field(
        default=None,
        metadata={
            "name": "ChargingSession",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evtermination_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "EVTerminationCode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 80,
        }
    )
    evtermination_explanation: Optional[str] = field(
        default=None,
        metadata={
            "name": "EVTerminationExplanation",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 160,
        }
    )


@dataclass
class SessionStopResType(V2GresponseType):
    pass


@dataclass
class SignedCertificateChainType:
    certificate: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "Certificate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 1600,
            "format": "base64",
        }
    )
    sub_certificates: Optional[SubCertificatesType] = field(
        default=None,
        metadata={
            "name": "SubCertificates",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class SignedMeteringDataType:
    session_id: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "SessionID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "length": 8,
            "format": "base16",
        }
    )
    meter_info: Optional[MeterInfoType] = field(
        default=None,
        metadata={
            "name": "MeterInfo",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    receipt: Optional[ReceiptType] = field(
        default=None,
        metadata={
            "name": "Receipt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    dynamic_smdtcontrol_mode: Optional[DynamicSmdtcontrolModeType] = field(
        default=None,
        metadata={
            "name": "Dynamic_SMDTControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    scheduled_smdtcontrol_mode: Optional[ScheduledSmdtcontrolModeType] = field(
        default=None,
        metadata={
            "name": "Scheduled_SMDTControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class TaxRuleType:
    tax_rule_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "TaxRuleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )
    tax_rule_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxRuleName",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "max_length": 80,
        }
    )
    tax_rate: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "TaxRate",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    tax_included_in_price: Optional[bool] = field(
        default=None,
        metadata={
            "name": "TaxIncludedInPrice",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    applies_to_energy_fee: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AppliesToEnergyFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    applies_to_parking_fee: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AppliesToParkingFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    applies_to_overstay_fee: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AppliesToOverstayFee",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    applies_minimum_maximum_cost: Optional[bool] = field(
        default=None,
        metadata={
            "name": "AppliesMinimumMaximumCost",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class VehicleCheckInReqType(V2GrequestType):
    evcheck_in_status: Optional[EvCheckInStatusType] = field(
        default=None,
        metadata={
            "name": "EVCheckInStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    parking_method: Optional[ParkingMethodType] = field(
        default=None,
        metadata={
            "name": "ParkingMethod",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    vehicle_frame: Optional[int] = field(
        default=None,
        metadata={
            "name": "VehicleFrame",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    device_offset: Optional[int] = field(
        default=None,
        metadata={
            "name": "DeviceOffset",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    vehicle_travel: Optional[int] = field(
        default=None,
        metadata={
            "name": "VehicleTravel",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class VehicleCheckInResType(V2GresponseType):
    parking_space: Optional[int] = field(
        default=None,
        metadata={
            "name": "ParkingSpace",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    device_location: Optional[int] = field(
        default=None,
        metadata={
            "name": "DeviceLocation",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    target_distance: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetDistance",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class VehicleCheckOutReqType(V2GrequestType):
    evcheck_out_status: Optional[EvCheckOutStatusType] = field(
        default=None,
        metadata={
            "name": "EVCheckOutStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    check_out_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "CheckOutTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class VehicleCheckOutResType(V2GresponseType):
    evsecheck_out_status: Optional[EvseCheckOutStatusType] = field(
        default=None,
        metadata={
            "name": "EVSECheckOutStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class AdditionalServiceListType:
    additional_service: List[AdditionalServiceType] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 5,
        }
    )


@dataclass
class AuthorizationRes(AuthorizationResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class AuthorizationSetupReq(AuthorizationSetupReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class AuthorizationSetupResType(V2GresponseType):
    authorization_services: List[AuthorizationType] = field(
        default_factory=list,
        metadata={
            "name": "AuthorizationServices",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 2,
        }
    )
    certificate_installation_service: Optional[bool] = field(
        default=None,
        metadata={
            "name": "CertificateInstallationService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    eim_asres_authorization_mode: Optional[EimAsresAuthorizationModeType] = field(
        default=None,
        metadata={
            "name": "EIM_ASResAuthorizationMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    pn_c_asres_authorization_mode: Optional[PnCAsresAuthorizationModeType] = field(
        default=None,
        metadata={
            "name": "PnC_ASResAuthorizationMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class CertificateInstallationReqType(V2GrequestType):
    oemprovisioning_certificate_chain: Optional[SignedCertificateChainType] = field(
        default=None,
        metadata={
            "name": "OEMProvisioningCertificateChain",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    list_of_root_certificate_ids: Optional[ListOfRootCertificateIdsType] = field(
        default=None,
        metadata={
            "name": "ListOfRootCertificateIDs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    maximum_contract_certificate_chains: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaximumContractCertificateChains",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    prioritized_emaids: Optional[EmaidlistType] = field(
        default=None,
        metadata={
            "name": "PrioritizedEMAIDs",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class EvpowerProfileEntryListType:
    class Meta:
        name = "EVPowerProfileEntryListType"

    evpower_profile_entry: List[PowerScheduleEntryType] = field(
        default_factory=list,
        metadata={
            "name": "EVPowerProfileEntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 2048,
        }
    )


@dataclass
class EvpowerScheduleEntryListType:
    class Meta:
        name = "EVPowerScheduleEntryListType"

    evpower_schedule_entry: List[EvpowerScheduleEntryType] = field(
        default_factory=list,
        metadata={
            "name": "EVPowerScheduleEntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 1024,
        }
    )


@dataclass
class EvpriceRuleStackType:
    class Meta:
        name = "EVPriceRuleStackType"

    duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evprice_rule: List[EvpriceRuleType] = field(
        default_factory=list,
        metadata={
            "name": "EVPriceRule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 8,
        }
    )


@dataclass
class MeteringConfirmationReqType(V2GrequestType):
    signed_metering_data: Optional[SignedMeteringDataType] = field(
        default=None,
        metadata={
            "name": "SignedMeteringData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class MeteringConfirmationRes(MeteringConfirmationResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class OverstayRuleListType:
    overstay_time_threshold: Optional[int] = field(
        default=None,
        metadata={
            "name": "OverstayTimeThreshold",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    overstay_power_threshold: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "OverstayPowerThreshold",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    overstay_rule: List[OverstayRuleType] = field(
        default_factory=list,
        metadata={
            "name": "OverstayRule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 5,
        }
    )


@dataclass
class ParameterSetType:
    parameter_set_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ParameterSetID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    parameter: List[ParameterType] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 32,
        }
    )


@dataclass
class PnCAreqAuthorizationModeType:
    class Meta:
        name = "PnC_AReqAuthorizationModeType"

    gen_challenge: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "GenChallenge",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "length": 16,
            "format": "base64",
        }
    )
    contract_certificate_chain: Optional[ContractCertificateChainType] = field(
        default=None,
        metadata={
            "name": "ContractCertificateChain",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class PowerDeliveryRes(PowerDeliveryResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class PowerScheduleEntryListType:
    power_schedule_entry: List[PowerScheduleEntryType] = field(
        default_factory=list,
        metadata={
            "name": "PowerScheduleEntry",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 1024,
        }
    )


@dataclass
class PriceLevelScheduleType(PriceScheduleType):
    number_of_price_levels: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumberOfPriceLevels",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    price_level_schedule_entries: Optional[PriceLevelScheduleEntryListType] = field(
        default=None,
        metadata={
            "name": "PriceLevelScheduleEntries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class PriceRuleStackType:
    duration: Optional[int] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    price_rule: List[PriceRuleType] = field(
        default_factory=list,
        metadata={
            "name": "PriceRule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 8,
        }
    )


@dataclass
class ServiceDetailReq(ServiceDetailReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ServiceDiscoveryReq(ServiceDiscoveryReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ServiceDiscoveryResType(V2GresponseType):
    service_renegotiation_supported: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ServiceRenegotiationSupported",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    energy_transfer_service_list: Optional[ServiceListType] = field(
        default=None,
        metadata={
            "name": "EnergyTransferServiceList",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    vaslist: Optional[ServiceListType] = field(
        default=None,
        metadata={
            "name": "VASList",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ServiceSelectionReqType(V2GrequestType):
    selected_energy_transfer_service: Optional[SelectedServiceType] = field(
        default=None,
        metadata={
            "name": "SelectedEnergyTransferService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    selected_vaslist: Optional[SelectedServiceListType] = field(
        default=None,
        metadata={
            "name": "SelectedVASList",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ServiceSelectionRes(ServiceSelectionResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SessionSetupReq(SessionSetupReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SessionSetupRes(SessionSetupResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SessionStopReq(SessionStopReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SessionStopRes(SessionStopResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SignedInstallationDataType:
    contract_certificate_chain: Optional[ContractCertificateChainType] = field(
        default=None,
        metadata={
            "name": "ContractCertificateChain",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    ecdhcurve: Optional[EcdhCurveType] = field(
        default=None,
        metadata={
            "name": "ECDHCurve",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    dhpublic_key: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "DHPublicKey",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "length": 133,
            "format": "base64",
        }
    )
    secp521_encrypted_private_key: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "SECP521_EncryptedPrivateKey",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "length": 94,
            "format": "base64",
        }
    )
    x448_encrypted_private_key: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "X448_EncryptedPrivateKey",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "length": 84,
            "format": "base64",
        }
    )
    tpm_encrypted_private_key: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "TPM_EncryptedPrivateKey",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "length": 206,
            "format": "base64",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class SignedMeteringData(SignedMeteringDataType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class TaxRuleListType:
    tax_rule: List[TaxRuleType] = field(
        default_factory=list,
        metadata={
            "name": "TaxRule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 10,
        }
    )


@dataclass
class VehicleCheckInReq(VehicleCheckInReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class VehicleCheckInRes(VehicleCheckInResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class VehicleCheckOutReq(VehicleCheckOutReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class VehicleCheckOutRes(VehicleCheckOutResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class AuthorizationReqType(V2GrequestType):
    selected_authorization_service: Optional[AuthorizationType] = field(
        default=None,
        metadata={
            "name": "SelectedAuthorizationService",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    eim_areq_authorization_mode: Optional[EimAreqAuthorizationModeType] = field(
        default=None,
        metadata={
            "name": "EIM_AReqAuthorizationMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    pn_c_areq_authorization_mode: Optional[PnCAreqAuthorizationModeType] = field(
        default=None,
        metadata={
            "name": "PnC_AReqAuthorizationMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class AuthorizationSetupRes(AuthorizationSetupResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class CertificateInstallationReq(CertificateInstallationReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class CertificateInstallationResType(V2GresponseType):
    evseprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVSEProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    cpscertificate_chain: Optional[CertificateChainType] = field(
        default=None,
        metadata={
            "name": "CPSCertificateChain",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    signed_installation_data: Optional[SignedInstallationDataType] = field(
        default=None,
        metadata={
            "name": "SignedInstallationData",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    remaining_contract_certificate_chains: Optional[int] = field(
        default=None,
        metadata={
            "name": "RemainingContractCertificateChains",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class EvpowerProfileType:
    class Meta:
        name = "EVPowerProfileType"

    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    dynamic_evpptcontrol_mode: Optional[DynamicEvpptcontrolModeType] = field(
        default=None,
        metadata={
            "name": "Dynamic_EVPPTControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    scheduled_evpptcontrol_mode: Optional[ScheduledEvpptcontrolModeType] = field(
        default=None,
        metadata={
            "name": "Scheduled_EVPPTControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evpower_profile_entries: Optional[EvpowerProfileEntryListType] = field(
        default=None,
        metadata={
            "name": "EVPowerProfileEntries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class EvpowerScheduleType:
    class Meta:
        name = "EVPowerScheduleType"

    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evpower_schedule_entries: Optional[EvpowerScheduleEntryListType] = field(
        default=None,
        metadata={
            "name": "EVPowerScheduleEntries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class EvpriceRuleStackListType:
    class Meta:
        name = "EVPriceRuleStackListType"

    evprice_rule_stack: List[EvpriceRuleStackType] = field(
        default_factory=list,
        metadata={
            "name": "EVPriceRuleStack",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 1024,
        }
    )


@dataclass
class MeteringConfirmationReq(MeteringConfirmationReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class PowerScheduleType:
    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    available_energy: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "AvailableEnergy",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    power_tolerance: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "PowerTolerance",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    power_schedule_entries: Optional[PowerScheduleEntryListType] = field(
        default=None,
        metadata={
            "name": "PowerScheduleEntries",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class PriceRuleStackListType:
    price_rule_stack: List[PriceRuleStackType] = field(
        default_factory=list,
        metadata={
            "name": "PriceRuleStack",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 1024,
        }
    )


@dataclass
class ServiceDiscoveryRes(ServiceDiscoveryResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ServiceParameterListType:
    parameter_set: List[ParameterSetType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 32,
        }
    )


@dataclass
class ServiceSelectionReq(ServiceSelectionReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class SignedInstallationData(SignedInstallationDataType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class AbsolutePriceScheduleType(PriceScheduleType):
    currency: Optional[str] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 3,
        }
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 3,
        }
    )
    price_algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "PriceAlgorithm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 255,
        }
    )
    minimum_cost: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "MinimumCost",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    maximum_cost: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "MaximumCost",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    tax_rules: Optional[TaxRuleListType] = field(
        default=None,
        metadata={
            "name": "TaxRules",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    price_rule_stacks: Optional[PriceRuleStackListType] = field(
        default=None,
        metadata={
            "name": "PriceRuleStacks",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    overstay_rules: Optional[OverstayRuleListType] = field(
        default=None,
        metadata={
            "name": "OverstayRules",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    additional_selected_services: Optional[AdditionalServiceListType] = field(
        default=None,
        metadata={
            "name": "AdditionalSelectedServices",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class AuthorizationReq(AuthorizationReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class CertificateInstallationRes(CertificateInstallationResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class EvabsolutePriceScheduleType:
    class Meta:
        name = "EVAbsolutePriceScheduleType"

    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    currency: Optional[str] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 3,
        }
    )
    price_algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "PriceAlgorithm",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "max_length": 255,
        }
    )
    evprice_rule_stacks: Optional[EvpriceRuleStackListType] = field(
        default=None,
        metadata={
            "name": "EVPriceRuleStacks",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class PowerDeliveryReqType(V2GrequestType):
    evprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    charge_progress: Optional[ChargeProgressType] = field(
        default=None,
        metadata={
            "name": "ChargeProgress",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evpower_profile: Optional[EvpowerProfileType] = field(
        default=None,
        metadata={
            "name": "EVPowerProfile",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    bpt_channel_selection: Optional[ChannelSelectionType] = field(
        default=None,
        metadata={
            "name": "BPT_ChannelSelection",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ServiceDetailResType(V2GresponseType):
    service_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ServiceID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    service_parameter_list: Optional[ServiceParameterListType] = field(
        default=None,
        metadata={
            "name": "ServiceParameterList",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class ChargingScheduleType:
    power_schedule: Optional[PowerScheduleType] = field(
        default=None,
        metadata={
            "name": "PowerSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    absolute_price_schedule: Optional[AbsolutePriceScheduleType] = field(
        default=None,
        metadata={
            "name": "AbsolutePriceSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    price_level_schedule: Optional[PriceLevelScheduleType] = field(
        default=None,
        metadata={
            "name": "PriceLevelSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class DynamicSeresControlModeType:
    class Meta:
        name = "Dynamic_SEResControlModeType"

    departure_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "DepartureTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    minimum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "MinimumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    absolute_price_schedule: Optional[AbsolutePriceScheduleType] = field(
        default=None,
        metadata={
            "name": "AbsolutePriceSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    price_level_schedule: Optional[PriceLevelScheduleType] = field(
        default=None,
        metadata={
            "name": "PriceLevelSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class EvenergyOfferType:
    class Meta:
        name = "EVEnergyOfferType"

    evpower_schedule: Optional[EvpowerScheduleType] = field(
        default=None,
        metadata={
            "name": "EVPowerSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    evabsolute_price_schedule: Optional[EvabsolutePriceScheduleType] = field(
        default=None,
        metadata={
            "name": "EVAbsolutePriceSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )


@dataclass
class PowerDeliveryReq(PowerDeliveryReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ServiceDetailRes(ServiceDetailResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ScheduleTupleType:
    schedule_tuple_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ScheduleTupleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )
    charging_schedule: Optional[ChargingScheduleType] = field(
        default=None,
        metadata={
            "name": "ChargingSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    discharging_schedule: Optional[ChargingScheduleType] = field(
        default=None,
        metadata={
            "name": "DischargingSchedule",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ScheduledSereqControlModeType:
    class Meta:
        name = "Scheduled_SEReqControlModeType"

    departure_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "DepartureTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evtarget_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evmaximum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evminimum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    evenergy_offer: Optional[EvenergyOfferType] = field(
        default=None,
        metadata={
            "name": "EVEnergyOffer",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ScheduleExchangeReqType(V2GrequestType):
    maximum_supporting_points: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaximumSupportingPoints",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
            "min_inclusive": 12,
            "max_inclusive": 1024,
        }
    )
    dynamic_sereq_control_mode: Optional[DynamicSereqControlModeType] = field(
        default=None,
        metadata={
            "name": "Dynamic_SEReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    scheduled_sereq_control_mode: Optional[ScheduledSereqControlModeType] = field(
        default=None,
        metadata={
            "name": "Scheduled_SEReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ScheduledSeresControlModeType:
    class Meta:
        name = "Scheduled_SEResControlModeType"

    schedule_tuple: List[ScheduleTupleType] = field(
        default_factory=list,
        metadata={
            "name": "ScheduleTuple",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "min_occurs": 1,
            "max_occurs": 3,
        }
    )


@dataclass
class ScheduleExchangeReq(ScheduleExchangeReqType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"


@dataclass
class ScheduleExchangeResType(V2GresponseType):
    evseprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVSEProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
            "required": True,
        }
    )
    go_to_pause: Optional[bool] = field(
        default=None,
        metadata={
            "name": "GoToPause",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    dynamic_seres_control_mode: Optional[DynamicSeresControlModeType] = field(
        default=None,
        metadata={
            "name": "Dynamic_SEResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )
    scheduled_seres_control_mode: Optional[ScheduledSeresControlModeType] = field(
        default=None,
        metadata={
            "name": "Scheduled_SEResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonMessages",
        }
    )


@dataclass
class ScheduleExchangeRes(ScheduleExchangeResType):
    class Meta:
        namespace = "urn:iso:std:iso:15118:-20:CommonMessages"
