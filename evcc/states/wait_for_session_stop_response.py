"""
.. module:: wait_for_session_stop_response
   :platform: Unix
   :synopsis: A module describing the SessionStop state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, TerminateSession


class WaitForSessionStopResponse(EVState):
    def __init__(self):
        super(WaitForSessionStopResponse, self).__init__(name="WaitForSessionStopRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        return TerminateSession()
