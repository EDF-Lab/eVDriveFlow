"""
.. module:: wait_for_session_setup_response
   :platform: Unix
   :synopsis: A module describing the SessionSetup state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.log import logger
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from evcc.states.ev_state import EVState
from shared.xml_classes.common_messages import AuthorizationSetupReq, MessageHeaderType, ResponseCodeType
import time


class WaitForSessionSetupResponse(EVState):
    def __init__(self):
        super(WaitForSessionSetupResponse, self).__init__(name="WaitForSessionSetupRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = AuthorizationSetupReq()
        if payload.response_code == ResponseCodeType.OK_NEW_SESSION_ESTABLISHED:
            session_id = payload.header.session_id
            logger.info("Negotiated session id is: %s.", session_id)
            # TODO: handling reconnection to an older session
        request.header = MessageHeaderType(session_id, int(time.time()))
        extra_data["session_id"] = session_id
        reaction = SendMessage()
        reaction.message = request
        reaction.extra_data = extra_data
        return reaction

