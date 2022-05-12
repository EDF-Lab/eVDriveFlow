"""
.. module:: wait_for_authorization_setup_response
   :platform: Unix
   :synopsis: A module describing the AuthorizationSetup state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
import time
from shared.log import logger

from shared.xml_classes.common_messages import AuthorizationReq, AuthorizationType, MessageHeaderType


class WaitForAuthorizationSetupResponse(EVState):
    def __init__(self):
        super(WaitForAuthorizationSetupResponse, self).__init__(name="WaitForAuthorizationSetupRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = AuthorizationReq()
        logger.error(str(payload))
        logger.error(str(self.controller.data_model.authorization_services))
        for _ in payload.authorization_services:
            if _ in self.controller.data_model.authorization_services: #TODO: remove eim_asres_authorization_mode
                request.selected_authorization_service = AuthorizationType.EIM
                request.eim_areq_authorization_mode = ""
                extra_data["selected_authorization_service"] = AuthorizationType.EIM
            else:
                raise NotImplementedError
                # TODO other cases
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = request
        reaction.msg_type = "Common"
        return reaction
