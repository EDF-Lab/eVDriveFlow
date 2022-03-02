"""
.. module:: initial_state
   :platform: Unix
   :synopsis: A module describing an initial state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from secc.states.evse_state import EVSEState
from shared.reaction_message import ReactionToIncomingMessage


class InitialState(EVSEState):
    def __init__(self):
        super(InitialState, self).__init__(name="InitialState")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        pass
