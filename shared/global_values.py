"""
.. module:: global_values
   :platform: Unix
   :synopsis: A module that contains most of the shared global variables.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.

"""

# Some network settings
UDP_SERVER_PORT = 15118  # table 18, UDP server port
LOCAL_LINK_MULTICAST_ADDRESS = "ff02::1"

# Filepaths
EVCC_CERTCHAIN = "../shared/certificates/certs/vehicleCertChain.pem"
EVCC_KEYFILE = "../shared/certificates/privateKeys/vehicle.key"
EVCC_CERTIFICATE_AUTHORITY = "../shared/certificates/certs/oemRootCACert.pem"
SECC_CERTCHAIN = "../shared/certificates/certs/seccCertChain.pem"
SECC_KEYFILE = "../shared/certificates/privateKeys/secc.key"
SECC_CERTIFICATE_AUTHORITY = "../shared/certificates/certs/v2gRootCACert.pem"
APP_PROTOCOL_XSD = "../shared/xsd_files/latest_version/V2G_CI_AppProtocol.xsd"
COMMON_MESSAGES_XSD = "../shared/xsd_files/latest_version/V2G_CI_CommonMessages.xsd"
DC_MESSAGES_XSD = "../shared/xsd_files/latest_version/V2G_CI_DC.xsd"
APP_PROTOCOL_EXIG = "../shared/exig_files/latest_version/V2G_CI_AppProtocol.exig"
COMMON_MESSAGES_EXIG = "../shared/exig_files/latest_version/V2G_CI_CommonMessages.exig"
DC_MESSAGES_EXIG = "../shared/exig_files/latest_version/V2G_CI_DC.exig"

# Passphrase used to access private key. This parameter shall be stored in a secured directory.
PASSPHRASE = "123456789abcdefgh"

# Payload settings
PROTOCOL_VERSION = 0x01
SECURITY_PROTOCOL = 0x00  # Use 0x00 to enable TLS or 0x10 to disable TLS [Testing purposes]
MAX_PAYLOAD_LENGTH = 4294967295
SUPPORTED_CIPHER_SUITES_TLS_1_3 = "TLS_AES_256_GCM_SHA384:CHACHA20_POLY1305"
SDP_PAYLOAD_TYPES = {0x8001: "SAPPayloadID", 0x8002: "Part20MainstreamPayloadID", 0x8003: "Part20ACMainstreamPayloadID",
                     0x8004: "Part20DCMainstreamPayloadID", 0x8005: "Part20ACDPMainstreamPayloadID",
                     0x8006: "Part20WPTMainstreamPayloadID", 0x8101: "ScheduleRenegotiationPayloadID",
                     0x8102: "MeteringConfirmationPayloadID", 0x8103: "ACDSystemStatusPayloadID",
                     0x8104: "ParkingStatusPayloadID", 0x9000: "SDPRequestPayloadID", 0x9001: "SDPResponsePayloadID",
                     0x9002: "SDPRequestWithPPDPayloadID", 0x9003: "SDPResponseWithPPDPayloadID"}  # [7.8.3-3152]
V2G_CI_MSG_DC_NAMESPACE = "urn:iso:std:iso:15118:-20:DC"

# See table 214
EVCC_MSG_TIMEOUT = {"SupportedAppProtocolReq": 2, "SessionSetupReq": 2, "VehicleCheckInReq": 2, "VehicleCheckOut": 2,
                    "AuthorizationSetupReq": 2, "AuthorizationReq": 2, "CertificateInstallationReq": 5,
                    "ServiceDiscoveryReq": 2, "ServiceDetailReq": 5, "ServiceSelectionReq": 2,
                    "ChargeParameterDiscoveryReq": 2, "ScheduleExchangeReq": 2, "PowerDeliveryReq": 2,
                    "MeteringConfirmationReq": 2, "SessionStopReq": 2}
SECC_MSG_PERFORMANCE_TIME = {"SupportedAppProtocolReq": 1.5, "SessionSetupReq": 1.5, "VehicleCheckInReq": 1.5,
                             "VehicleCheckOutReq": 1.5, "AuthorizationSetupReq": 1.5, "AuthorizationReq": 1.5,
                             "CertificateInstallationReq": 4.5, "ServiceDiscoveryReq": 1.5, "ServiceDetailReq": 4.5,
                             "ServiceSelectionReq": 1.5, "ChargeParameterDiscoveryReq": 1.5,
                             "ScheduleExchangeReq": 1.5, "PowerDeliveryReq": 1.5, "MeteringConfirmationReq": 1.5,
                             "SessionStopReq": 1.5}
EVCC_SEQUENCE_PERFORMANCE_TIME = 40
SECC_SEQUENCE_TIMEOUT = 60
EVCC_ONGOING_TIMEOUT = 60
SECC_ONGOING_TIMEOUT = 60
EVCC_ONGOING_PERFORMANCE_TIME = 55
SECC_ONGOING_PERFORMANCE_TIME = 55

# See table 216
DC_EVCC_MSG_TIMEOUT = {"DcCableCheckReq": 2, "DcPreChargeReq": 2, "DcChargeLoopReq": 0.5, "DcWeldingDetectionReq": 2,
                       "DcChargeParameterDiscoveryReq": 2}  # the last one was added (standard define common timeout for AC)
DC_SECC_MSG_PERFORMANCE_TIME = {"DcCableCheckReq": 1.5, "DcPreChargeReq": 1.5, "DcChargeLoopReq": 0.25,
                                "DcWeldingDetectionReq": 1.5, "DcChargeParameterDiscoveryReq": 1.5}  # same as above
DC_EVCC_SEQUENCE_PERFORMANCE_TIME = {"DcChargeLoopReq": 0.25}
DC_SECC_SEQUENCE_TIMEOUT = {"DcChargeLoopRes": 0.5}
