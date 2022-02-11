"""
.. module:: payloads
   :platform: Unix
   :synopsis: A module that describes 15118 messages' payloads.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from scapy.all import Packet, XIntField, XStrLenField, IP6Field, XShortField, XByteField


class Payload(Packet):
    """This is the basic payload class for V2G messages.

    """
    name = "Payload"


class EXIPayload(Payload):
    """This is the payload for EXI format contents.

    """
    name = "EXI"
    fields_desc = [XIntField("payloadLength", None),
                   XStrLenField("payloadContent", "", length_from=lambda pkt: pkt.payloadLength, max_length=4294967295)
                   ]

    def post_build(self, pkt: Packet, pay: Packet) -> Packet:
        """Allows calculation of the payload's length after it's been built.

        :param pkt: The current layer.
        :param pay: The actual payload.
        :return : pkt + pay -- concatenation of layers.

        """
        if self.payloadLength is None:
            if pay:
                length = len(pay)
            else:
                length = len(self.getfieldval("payloadContent"))
            pkt = pkt[:0] + length.to_bytes(4, 'big') + pkt[4:]
        return pkt + pay


class SDPResPayload(Payload):
    """This is the payload for SECC Discovery Protocol Response.
        0x00: TCP Transport Protocol
        0x00: Security secured with TLS

    """
    name = "SDPRes"
    fields_desc = [XIntField("PayloadLength", 20),
                   IP6Field("TargetAddress", "::"),
                   XShortField("TargetPort", 0),
                   XByteField("SecurityProtocol", 0x00),
                   XByteField("TransportProtocol", 0x00)]


class SDPReqPayload(Payload):
    """This is the payload for SECC Discovery Protocol Request.
        0x00: TCP Transport Protocol
        0x00: Security secured with TLS

    """
    name = "SDPReq"
    fields_desc = [XIntField("PayloadLength", 2),
                   XByteField("SecurityProtocol", 0x00),
                   XByteField("TransportProtocol", 0x00)]
