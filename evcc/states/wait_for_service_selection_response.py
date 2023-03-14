"""
.. module:: wait_for_service_selection_response
   :platform: Unix
   :synopsis: A module describing the ServiceSelection state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import EVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.dc import MessageHeaderType
import time
from shared.xml_classes.dc import DcChargeParameterDiscoveryReq


class WaitForServiceSelectionResponse(EVState):
    def __init__(self):
        super(WaitForServiceSelectionResponse, self).__init__(name="WaitForServiceSelectionRes")

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        request = DcChargeParameterDiscoveryReq()
        request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
        if self.session_parameters.dc_bpt_selected == True:
            request.bpt_dc_cpdreq_energy_transfer_mode = self.controller.data_model.get_bpt_dc_cpdreq_energy_transfer_mode()
        else :
            request.dc_cpdreq_energy_transfer_mode = self.controller.data_model.get_dc_cpdreq_energy_transfer_mode()
        
        reaction = SendMessage()
        reaction.extra_data = extra_data
        reaction.message = request
        reaction.msg_type = "DC"
        return reaction
