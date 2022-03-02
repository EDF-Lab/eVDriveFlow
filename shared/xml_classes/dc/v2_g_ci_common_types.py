from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from shared.xml_classes.dc.xmldsig_core_schema import (
    Signature,
    X509IssuerSerialType,
)

__NAMESPACE__ = "urn:iso:std:iso:15118:-20:CommonTypes"


@dataclass
class ClreqControlModeType:
    class Meta:
        name = "CLReqControlModeType"


@dataclass
class ClresControlModeType:
    class Meta:
        name = "CLResControlModeType"


@dataclass
class MeterInfoType:
    meter_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MeterID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
            "max_length": 32,
        }
    )
    charged_energy_reading_wh: Optional[int] = field(
        default=None,
        metadata={
            "name": "ChargedEnergyReadingWh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    bpt_discharged_energy_reading_wh: Optional[int] = field(
        default=None,
        metadata={
            "name": "BPT_DischargedEnergyReadingWh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    capacitive_energy_reading_varh: Optional[int] = field(
        default=None,
        metadata={
            "name": "CapacitiveEnergyReadingVARh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    bpt_inductive_energy_reading_varh: Optional[int] = field(
        default=None,
        metadata={
            "name": "BPT_InductiveEnergyReadingVARh",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    meter_signature: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "MeterSignature",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "max_length": 64,
            "format": "base64",
        }
    )
    meter_status: Optional[int] = field(
        default=None,
        metadata={
            "name": "MeterStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    meter_timestamp: Optional[int] = field(
        default=None,
        metadata={
            "name": "MeterTimestamp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class RationalNumberType:
    exponent: Optional[int] = field(
        default=None,
        metadata={
            "name": "Exponent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


class EvseNotificationType(Enum):
    PAUSE = "Pause"
    EXIT_STANDBY = "ExitStandby"
    TERMINATE = "Terminate"
    SCHEDULE_RENEGOTIATION = "ScheduleRenegotiation"
    SERVICE_RENEGOTIATION = "ServiceRenegotiation"
    METERING_CONFIRMATION = "MeteringConfirmation"


class ProcessingType(Enum):
    FINISHED = "Finished"
    ONGOING = "Ongoing"
    ONGOING_WAITING_FOR_CUSTOMER_INTERACTION = "Ongoing_WaitingForCustomerInteraction"


class ResponseCodeType(Enum):
    OK = "OK"
    OK_NEW_SESSION_ESTABLISHED = "OK_NewSessionEstablished"
    OK_OLD_SESSION_JOINED = "OK_OldSessionJoined"
    OK_CERTIFICATE_EXPIRES_SOON = "OK_CertificateExpiresSoon"
    OK_ISOLATION_VALID = "OK_IsolationValid"
    OK_ISOLATION_WARNING = "OK_IsolationWarning"
    WARNING_CERTIFICATE_EXPIRED = "WARNING_CertificateExpired"
    WARNING_NO_CERTIFICATE_AVAILABLE = "WARNING_NoCertificateAvailable"
    WARNING_CERTIFICATE_VALIDATION_ERROR = "WARNING_CertificateValidationError"
    WARNING_E_MSPUNKNOWN = "WARNING_eMSPUnknown"
    WARNING_CERTIFICATE_NOT_YET_VALID = "WARNING_CertificateNotYetValid"
    WARNING_CERTIFICATE_REVOKED = "WARNING_CertificateRevoked"
    WARNING_CHALLENGE_INVALID = "WARNING_ChallengeInvalid"
    WARNING_GENERAL_PN_CAUTHORIZATION_ERROR = "WARNING_GeneralPnCAuthorizationError"
    WARNING_AUTHORIZATION_SELECTION_INVALID = "WARNING_AuthorizationSelectionInvalid"
    WARNING_WPT = "WARNING_WPT"
    FAILED = "FAILED"
    FAILED_SEQUENCE_ERROR = "FAILED_SequenceError"
    FAILED_PAUSE_NOT_ALLOWED = "FAILED_PauseNotAllowed"
    FAILED_SERVICE_IDINVALID = "FAILED_ServiceIDInvalid"
    FAILED_UNKNOWN_SESSION = "FAILED_UnknownSession"
    FAILED_SERVICE_SELECTION_INVALID = "FAILED_ServiceSelectionInvalid"
    FAILED_SIGNATURE_ERROR = "FAILED_SignatureError"
    FAILED_AUTHORIZATION_SELECTION_INVALID = "FAILED_AuthorizationSelectionInvalid"
    FAILED_WRONG_CHARGE_PARAMETER = "FAILED_WrongChargeParameter"
    FAILED_ISOLATION_FAULT = "FAILED_IsolationFault"
    FAILED_POWER_DELIVERY_NOT_APPLIED = "FAILED_PowerDeliveryNotApplied"
    FAILED_TARIFF_SELECTION_INVALID = "FAILED_TariffSelectionInvalid"
    FAILED_CHARGING_PROFILE_INVALID = "FAILED_ChargingProfileInvalid"
    FAILED_METERING_SIGNATURE_NOT_VALID = "FAILED_MeteringSignatureNotValid"
    FAILED_NO_CHARGE_SERVICE_SELECTED = "FAILED_NoChargeServiceSelected"
    FAILED_CONTACTOR_ERROR = "FAILED_ContactorError"
    FAILED_CERTIFICATE_NOT_YET_VALID = "FAILED_CertificateNotYetValid"


@dataclass
class ClreqControlMode(ClreqControlModeType):
    class Meta:
        name = "CLReqControlMode"
        namespace = "urn:iso:std:iso:15118:-20:CommonTypes"


@dataclass
class ClresControlMode(ClresControlModeType):
    class Meta:
        name = "CLResControlMode"
        namespace = "urn:iso:std:iso:15118:-20:CommonTypes"


@dataclass
class DetailedCostType:
    amount: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    cost_per_unit: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "CostPerUnit",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class DetailedTaxType:
    tax_rule_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "TaxRuleID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 4294967295,
        }
    )
    amount: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class DisplayParametersType:
    present_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "PresentSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    minimum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "MinimumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    maximum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaximumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    remaining_time_to_minimum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "RemainingTimeToMinimumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    remaining_time_to_target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "RemainingTimeToTargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    remaining_time_to_maximum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "RemainingTimeToMaximumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    charging_complete: Optional[bool] = field(
        default=None,
        metadata={
            "name": "ChargingComplete",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    battery_energy_capacity: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "BatteryEnergyCapacity",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    inlet_hot: Optional[bool] = field(
        default=None,
        metadata={
            "name": "InletHot",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class DynamicClreqControlModeType(ClreqControlModeType):
    class Meta:
        name = "Dynamic_CLReqControlModeType"

    departure_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "DepartureTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    evtarget_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    evmaximum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    evminimum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class DynamicClresControlModeType(ClresControlModeType):
    class Meta:
        name = "Dynamic_CLResControlModeType"

    departure_time: Optional[int] = field(
        default=None,
        metadata={
            "name": "DepartureTime",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    minimum_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "MinimumSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )
    ack_max_delay: Optional[int] = field(
        default=None,
        metadata={
            "name": "AckMaxDelay",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class EvsestatusType:
    class Meta:
        name = "EVSEStatusType"

    notification_max_delay: Optional[int] = field(
        default=None,
        metadata={
            "name": "NotificationMaxDelay",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    evsenotification: Optional[EvseNotificationType] = field(
        default=None,
        metadata={
            "name": "EVSENotification",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class ListOfRootCertificateIdsType:
    class Meta:
        name = "ListOfRootCertificateIDsType"

    root_certificate_id: List[X509IssuerSerialType] = field(
        default_factory=list,
        metadata={
            "name": "RootCertificateID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "min_occurs": 1,
            "max_occurs": 20,
        }
    )


@dataclass
class MessageHeaderType:
    session_id: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "SessionID",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
            "length": 8,
            "format": "base16",
        }
    )
    time_stamp: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeStamp",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    signature: Optional[Signature] = field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )


@dataclass
class ScheduledClreqControlModeType(ClreqControlModeType):
    class Meta:
        name = "Scheduled_CLReqControlModeType"

    evtarget_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    evmaximum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    evminimum_energy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class ScheduledClresControlModeType(ClresControlModeType):
    class Meta:
        name = "Scheduled_CLResControlModeType"


@dataclass
class ReceiptType:
    time_anchor: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeAnchor",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )
    energy_costs: Optional[DetailedCostType] = field(
        default=None,
        metadata={
            "name": "EnergyCosts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    occupancy_costs: Optional[DetailedCostType] = field(
        default=None,
        metadata={
            "name": "OccupancyCosts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    additional_services_costs: Optional[DetailedCostType] = field(
        default=None,
        metadata={
            "name": "AdditionalServicesCosts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    overstay_costs: Optional[DetailedCostType] = field(
        default=None,
        metadata={
            "name": "OverstayCosts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    tax_costs: List[DetailedTaxType] = field(
        default_factory=list,
        metadata={
            "name": "TaxCosts",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "max_occurs": 10,
        }
    )


@dataclass
class V2GmessageType:
    class Meta:
        name = "V2GMessageType"

    header: Optional[MessageHeaderType] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class V2GrequestType(V2GmessageType):
    class Meta:
        name = "V2GRequestType"


@dataclass
class V2GresponseType(V2GmessageType):
    class Meta:
        name = "V2GResponseType"

    response_code: Optional[ResponseCodeType] = field(
        default=None,
        metadata={
            "name": "ResponseCode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class ChargeLoopReqType(V2GrequestType):
    display_parameters: Optional[DisplayParametersType] = field(
        default=None,
        metadata={
            "name": "DisplayParameters",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    meter_info_requested: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MeterInfoRequested",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
            "required": True,
        }
    )


@dataclass
class ChargeLoopResType(V2GresponseType):
    evsestatus: Optional[EvsestatusType] = field(
        default=None,
        metadata={
            "name": "EVSEStatus",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    meter_info: Optional[MeterInfoType] = field(
        default=None,
        metadata={
            "name": "MeterInfo",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )
    receipt: Optional[ReceiptType] = field(
        default=None,
        metadata={
            "name": "Receipt",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class ChargeParameterDiscoveryReqType(V2GrequestType):
    pass


@dataclass
class ChargeParameterDiscoveryResType(V2GresponseType):
    pass
