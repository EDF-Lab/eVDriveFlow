"""
.. module:: process_authorization_setup_request
   :platform: Unix
   :synopsis: A module describing the AuthorizationSetup state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import AuthorizationSetupRes, MessageHeaderType, ResponseCodeType
import time


class ProcessAuthorizationSetupRequest(EVSEState):
    def __init__(self):
        super(ProcessAuthorizationSetupRequest, self).__init__(name="ProcessAuthorizationSetupReq")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        response = AuthorizationSetupRes()
        response.authorization_services = self.controller.data_model.authorization_services
        response.certificate_installation_service = self.controller.data_model.certificate_installation_service
        # TODO: given the services in authorization services, the response shall be eim or pnc
        response.eim_asres_authorization_mode = ""
        response.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        response.response_code = ResponseCodeType.OK
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = response
        reaction.msg_type = "Common"
        return reaction
