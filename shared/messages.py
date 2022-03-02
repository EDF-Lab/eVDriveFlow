"""
.. module:: messages
   :platform: Unix
   :synopsis: A module that describes 15118 messages.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from scapy.all import Packet, XByteField, bind_layers, UDP, XShortEnumField
from shared.payloads import EXIPayload, SDPResPayload, SDPReqPayload
from shared.global_values import SDP_PAYLOAD_TYPES, UDP_SERVER_PORT
from abc import abstractmethod


class V2GTPMessage(Packet):
    """This is the class that represents V2G messages.

    """
    name = "V2GTP"
    fields_desc = [XByteField("protocolVersion", 0x01),
                   XByteField("inverseProtocolVersion", 0xfe),
                   XShortEnumField("payloadType", 0x8001, SDP_PAYLOAD_TYPES)
                   ]

    def get_protocol_version(self):
        return self.getfieldval("protocolVersion")

    def get_inverse_protocol_version(self):
        return self.getfieldval("inverseProtocolVersion")

    def get_payload_type(self):
        return self.getfieldval("payloadType")

    def get_payload_length(self):
        return len(self.payload) - 4  # minus 4 because the payload contains the size of the payload as well (int)

    @abstractmethod
    def fill(self):
        pass


class SupportedAppMessage(V2GTPMessage):
    """This is a class that represents SupportedAppProtocol messages. Inherits from V2GTPMessage.

    """
    def fill(self):
        raise NotImplementedError


class EXIMessage(V2GTPMessage):
    """This is a class that represents the messages that have an EXI payload. Inherits from V2GTPMessage.

    """
    def fill(self):
        raise NotImplementedError


class EXIDCMessage(V2GTPMessage):
    """This is a class that represents the messages that have an EXI payload. Inherits from V2GTPMessage.

    """
    def fill(self):
        raise NotImplementedError


class SDPMessage(V2GTPMessage):
    """This is a class that represents SECC Discovery Protocol messages. Inherits from V2GTPMessage.

    """
    def fill(self):
        raise NotImplementedError


# This part binds the layers together. In each message type, there is a spcific payload. When creating the packets, we
# need to do it this way: EXIMessage()/EXIPayload. When doing so, thanks to the code below, the payloadType value will
# automatically become 0x8002 instead of the 0x8001 default value. This is done so that we don't have to fiddle with
# the payloadType when creating a new message.
bind_layers(EXIMessage, EXIPayload, {"payloadType": 0x8002})
bind_layers(SupportedAppMessage, EXIPayload, {"payloadType": 0x8001})
bind_layers(EXIDCMessage, EXIPayload, {"payloadType": 0x8004})
bind_layers(SDPMessage, SDPReqPayload, {'payloadType': 0x9000})
bind_layers(SDPMessage, SDPResPayload, {'payloadType': 0x9001})
bind_layers(UDP, SDPMessage, {"dport": UDP_SERVER_PORT})
bind_layers(UDP, SDPMessage, {"sport": UDP_SERVER_PORT})

