from dataclasses import dataclass, field
from typing import Optional
from shared.xml_classes.dc.v2_g_ci_common_types import (
    ClreqControlMode,
    ClresControlMode,
    ChargeLoopReqType,
    ChargeLoopResType,
    ChargeParameterDiscoveryReqType,
    ChargeParameterDiscoveryResType,
    DynamicClreqControlModeType,
    DynamicClresControlModeType,
    RationalNumberType,
    ScheduledClreqControlModeType,
    ScheduledClresControlModeType,
    V2GrequestType,
    V2GresponseType,
    ProcessingType,
)

__NAMESPACE__ = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcCpdreqEnergyTransferModeType:
    class Meta:
        name = "DC_CPDReqEnergyTransferModeType"

    evmaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    target_soc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TargetSOC",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "min_inclusive": 0,
            "max_inclusive": 100,
        }
    )


@dataclass
class DcCpdresEnergyTransferModeType:
    class Meta:
        name = "DC_CPDResEnergyTransferModeType"

    evsemaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsepower_ramp_limitation: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEPowerRampLimitation",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class DcCableCheckReqType(V2GrequestType):
    class Meta:
        name = "DC_CableCheckReqType"


@dataclass
class DcCableCheckResType(V2GresponseType):
    class Meta:
        name = "DC_CableCheckResType"

    evseprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVSEProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DcPreChargeReqType(V2GrequestType):
    class Meta:
        name = "DC_PreChargeReqType"

    evprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evpresent_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVPresentVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evtarget_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DcPreChargeResType(V2GresponseType):
    class Meta:
        name = "DC_PreChargeResType"

    evsepresent_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEPresentVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DcWeldingDetectionReqType(V2GrequestType):
    class Meta:
        name = "DC_WeldingDetectionReqType"

    evprocessing: Optional[ProcessingType] = field(
        default=None,
        metadata={
            "name": "EVProcessing",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DcWeldingDetectionResType(V2GresponseType):
    class Meta:
        name = "DC_WeldingDetectionResType"

    evsepresent_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEPresentVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DynamicDcClreqControlModeType(DynamicClreqControlModeType):
    class Meta:
        name = "Dynamic_DC_CLReqControlModeType"

    evmaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class DynamicDcClresControlModeType(DynamicClresControlModeType):
    class Meta:
        name = "Dynamic_DC_CLResControlModeType"

    evsemaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class ScheduledDcClreqControlModeType(ScheduledClreqControlModeType):
    class Meta:
        name = "Scheduled_DC_CLReqControlModeType"

    evtarget_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evtarget_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVTargetVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evmaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evmaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class ScheduledDcClresControlModeType(ScheduledClresControlModeType):
    class Meta:
        name = "Scheduled_DC_CLResControlModeType"

    evsemaximum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evseminimum_charge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumChargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evsemaximum_charge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumChargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evsemaximum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class BptDcCpdreqEnergyTransferModeType(DcCpdreqEnergyTransferModeType):
    class Meta:
        name = "BPT_DC_CPDReqEnergyTransferModeType"

    evmaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class BptDcCpdresEnergyTransferModeType(DcCpdresEnergyTransferModeType):
    class Meta:
        name = "BPT_DC_CPDResEnergyTransferModeType"

    evsemaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class BptDynamicDcClreqControlModeType(DynamicDcClreqControlModeType):
    class Meta:
        name = "BPT_Dynamic_DC_CLReqControlModeType"

    evmaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evmaximum_v2_xenergy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumV2XEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evminimum_v2_xenergy_request: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumV2XEnergyRequest",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class BptDynamicDcClresControlModeType(DynamicDcClresControlModeType):
    class Meta:
        name = "BPT_Dynamic_DC_CLResControlModeType"

    evsemaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsemaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evseminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )


@dataclass
class BptScheduledDcClreqControlModeType(ScheduledDcClreqControlModeType):
    class Meta:
        name = "BPT_Scheduled_DC_CLReqControlModeType"

    evmaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evmaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class BptScheduledDcClresControlModeType(ScheduledDcClresControlModeType):
    class Meta:
        name = "BPT_Scheduled_DC_CLResControlModeType"

    evsemaximum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evseminimum_discharge_power: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumDischargePower",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evsemaximum_discharge_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMaximumDischargeCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    evseminimum_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEMinimumVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class DcCpdreqEnergyTransferMode(DcCpdreqEnergyTransferModeType):
    class Meta:
        name = "DC_CPDReqEnergyTransferMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcCpdresEnergyTransferMode(DcCpdresEnergyTransferModeType):
    class Meta:
        name = "DC_CPDResEnergyTransferMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcCableCheckReq(DcCableCheckReqType):
    class Meta:
        name = "DC_CableCheckReq"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcCableCheckRes(DcCableCheckResType):
    class Meta:
        name = "DC_CableCheckRes"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcPreChargeReq(DcPreChargeReqType):
    class Meta:
        name = "DC_PreChargeReq"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcPreChargeRes(DcPreChargeResType):
    class Meta:
        name = "DC_PreChargeRes"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcWeldingDetectionReq(DcWeldingDetectionReqType):
    class Meta:
        name = "DC_WeldingDetectionReq"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcWeldingDetectionRes(DcWeldingDetectionResType):
    class Meta:
        name = "DC_WeldingDetectionRes"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DynamicDcClreqControlMode(DynamicDcClreqControlModeType):
    class Meta:
        name = "Dynamic_DC_CLReqControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DynamicDcClresControlMode(DynamicDcClresControlModeType):
    class Meta:
        name = "Dynamic_DC_CLResControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class ScheduledDcClreqControlMode(ScheduledDcClreqControlModeType):
    class Meta:
        name = "Scheduled_DC_CLReqControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class ScheduledDcClresControlMode(ScheduledDcClresControlModeType):
    class Meta:
        name = "Scheduled_DC_CLResControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptDcCpdreqEnergyTransferMode(BptDcCpdreqEnergyTransferModeType):
    class Meta:
        name = "BPT_DC_CPDReqEnergyTransferMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptDcCpdresEnergyTransferMode(BptDcCpdresEnergyTransferModeType):
    class Meta:
        name = "BPT_DC_CPDResEnergyTransferMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptDynamicDcClreqControlMode(BptDynamicDcClreqControlModeType):
    class Meta:
        name = "BPT_Dynamic_DC_CLReqControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptDynamicDcClresControlMode(BptDynamicDcClresControlModeType):
    class Meta:
        name = "BPT_Dynamic_DC_CLResControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptScheduledDcClreqControlMode(BptScheduledDcClreqControlModeType):
    class Meta:
        name = "BPT_Scheduled_DC_CLReqControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class BptScheduledDcClresControlMode(BptScheduledDcClresControlModeType):
    class Meta:
        name = "BPT_Scheduled_DC_CLResControlMode"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcChargeLoopReqType(ChargeLoopReqType):
    class Meta:
        name = "DC_ChargeLoopReqType"

    evpresent_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVPresentVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    bpt_dynamic_dc_clreq_control_mode: Optional[BptDynamicDcClreqControlMode] = field(
        default=None,
        metadata={
            "name": "BPT_Dynamic_DC_CLReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    dynamic_dc_clreq_control_mode: Optional[DynamicDcClreqControlMode] = field(
        default=None,
        metadata={
            "name": "Dynamic_DC_CLReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    bpt_scheduled_dc_clreq_control_mode: Optional[BptScheduledDcClreqControlMode] = field(
        default=None,
        metadata={
            "name": "BPT_Scheduled_DC_CLReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    scheduled_dc_clreq_control_mode: Optional[ScheduledDcClreqControlMode] = field(
        default=None,
        metadata={
            "name": "Scheduled_DC_CLReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    clreq_control_mode: Optional[ClreqControlMode] = field(
        default=None,
        metadata={
            "name": "CLReqControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class DcChargeLoopResType(ChargeLoopResType):
    class Meta:
        name = "DC_ChargeLoopResType"

    evsepresent_current: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEPresentCurrent",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsepresent_voltage: Optional[RationalNumberType] = field(
        default=None,
        metadata={
            "name": "EVSEPresentVoltage",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsepower_limit_achieved: Optional[bool] = field(
        default=None,
        metadata={
            "name": "EVSEPowerLimitAchieved",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsecurrent_limit_achieved: Optional[bool] = field(
        default=None,
        metadata={
            "name": "EVSECurrentLimitAchieved",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    evsevoltage_limit_achieved: Optional[bool] = field(
        default=None,
        metadata={
            "name": "EVSEVoltageLimitAchieved",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
            "required": True,
        }
    )
    bpt_dynamic_dc_clres_control_mode: Optional[BptDynamicDcClresControlMode] = field(
        default=None,
        metadata={
            "name": "BPT_Dynamic_DC_CLResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    dynamic_dc_clres_control_mode: Optional[DynamicDcClresControlMode] = field(
        default=None,
        metadata={
            "name": "Dynamic_DC_CLResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    bpt_scheduled_dc_clres_control_mode: Optional[BptScheduledDcClresControlMode] = field(
        default=None,
        metadata={
            "name": "BPT_Scheduled_DC_CLResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    scheduled_dc_clres_control_mode: Optional[ScheduledDcClresControlMode] = field(
        default=None,
        metadata={
            "name": "Scheduled_DC_CLResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    clres_control_mode: Optional[ClresControlMode] = field(
        default=None,
        metadata={
            "name": "CLResControlMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:CommonTypes",
        }
    )


@dataclass
class DcChargeParameterDiscoveryReqType(ChargeParameterDiscoveryReqType):
    class Meta:
        name = "DC_ChargeParameterDiscoveryReqType"

    bpt_dc_cpdreq_energy_transfer_mode: Optional[BptDcCpdreqEnergyTransferMode] = field(
        default=None,
        metadata={
            "name": "BPT_DC_CPDReqEnergyTransferMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    dc_cpdreq_energy_transfer_mode: Optional[DcCpdreqEnergyTransferMode] = field(
        default=None,
        metadata={
            "name": "DC_CPDReqEnergyTransferMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class DcChargeParameterDiscoveryResType(ChargeParameterDiscoveryResType):
    class Meta:
        name = "DC_ChargeParameterDiscoveryResType"

    bpt_dc_cpdres_energy_transfer_mode: Optional[BptDcCpdresEnergyTransferMode] = field(
        default=None,
        metadata={
            "name": "BPT_DC_CPDResEnergyTransferMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )
    dc_cpdres_energy_transfer_mode: Optional[DcCpdresEnergyTransferMode] = field(
        default=None,
        metadata={
            "name": "DC_CPDResEnergyTransferMode",
            "type": "Element",
            "namespace": "urn:iso:std:iso:15118:-20:DC",
        }
    )


@dataclass
class DcChargeLoopReq(DcChargeLoopReqType):
    class Meta:
        name = "DC_ChargeLoopReq"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcChargeLoopRes(DcChargeLoopResType):
    class Meta:
        name = "DC_ChargeLoopRes"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcChargeParameterDiscoveryReq(DcChargeParameterDiscoveryReqType):
    class Meta:
        name = "DC_ChargeParameterDiscoveryReq"
        namespace = "urn:iso:std:iso:15118:-20:DC"


@dataclass
class DcChargeParameterDiscoveryRes(DcChargeParameterDiscoveryResType):
    class Meta:
        name = "DC_ChargeParameterDiscoveryRes"
        namespace = "urn:iso:std:iso:15118:-20:DC"
