from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "urn:iso:15118:2:2010:AppProtocol"


@dataclass
class AppProtocolType:
    protocol_namespace: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProtocolNamespace",
            "type": "Element",
            "namespace": "",
            "required": True,
            "max_length": 100,
        }
    )
    version_number_major: Optional[int] = field(
        default=None,
        metadata={
            "name": "VersionNumberMajor",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    version_number_minor: Optional[int] = field(
        default=None,
        metadata={
            "name": "VersionNumberMinor",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    schema_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "SchemaID",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Element",
            "namespace": "",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 20,
        }
    )


class ResponseCodeType(Enum):
    OK_SUCCESSFUL_NEGOTIATION = "OK_SuccessfulNegotiation"
    OK_SUCCESSFUL_NEGOTIATION_WITH_MINOR_DEVIATION = "OK_SuccessfulNegotiationWithMinorDeviation"
    FAILED_NO_NEGOTIATION = "Failed_NoNegotiation"


@dataclass
class SupportedAppProtocolReq:
    class Meta:
        name = "supportedAppProtocolReq"
        namespace = "urn:iso:15118:2:2010:AppProtocol"

    app_protocol: List[AppProtocolType] = field(
        default_factory=list,
        metadata={
            "name": "AppProtocol",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
            "max_occurs": 20,
        }
    )


@dataclass
class SupportedAppProtocolRes:
    class Meta:
        name = "supportedAppProtocolRes"
        namespace = "urn:iso:15118:2:2010:AppProtocol"

    response_code: Optional[ResponseCodeType] = field(
        default=None,
        metadata={
            "name": "ResponseCode",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    schema_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "SchemaID",
            "type": "Element",
            "namespace": "",
        }
    )
