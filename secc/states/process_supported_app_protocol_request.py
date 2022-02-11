"""
.. module:: process_supported_app_protocol_request
   :platform: Unix
   :synopsis: A module describing the SupportedAppProtocol state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""


from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from secc.states.evse_state import EVSEState
from shared.xml_classes.app_protocol import SupportedAppProtocolReq, SupportedAppProtocolRes, ResponseCodeType


class ProcessSupportedAppProtocolRequest(EVSEState):
    def __init__(self):
        super(ProcessSupportedAppProtocolRequest, self).__init__(name="ProcessSupportedAppProtocolReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        match = False
        extra_data = {}
        response_code = ResponseCodeType.FAILED_NO_NEGOTIATION
        response = SupportedAppProtocolRes()
        if isinstance(payload, SupportedAppProtocolReq):
            # Sorting app protocols by priority
            payload.app_protocol.sort(key=self.get_priority)
            for protocol in payload.app_protocol:
                for supported_protocol in self.get_supported_app_protocols():
                    if protocol.protocol_namespace == supported_protocol.protocol_namespace and \
                            protocol.version_number_major == supported_protocol.version_number_major:
                        if protocol.version_number_minor == supported_protocol.version_number_minor:
                            response_code = ResponseCodeType.OK_SUCCESSFUL_NEGOTIATION
                        else:
                            response_code = ResponseCodeType.OK_SUCCESSFUL_NEGOTIATION_WITH_MINOR_DEVIATION
                        match = True
                        response.schema_id = protocol.schema_id
                        # Saving schema id in session
                        extra_data['schema_id'] = protocol.schema_id
                        break
                if match:
                    break
        response.response_code = response_code
        reaction = SendMessage()
        reaction.message = response
        reaction.extra_data = extra_data
        return reaction

    @staticmethod
    def get_priority(app_protocol):
        return app_protocol.priority

    def get_supported_app_protocols(self):
        return self.controller.data_model.supported_app_protocols
