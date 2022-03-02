"""
.. module:: wait_for_pre_charge_response
   :platform: Unix
   :synopsis: A module describing the PreCharge state.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from evcc.states.ev_state import DcEVState
from shared.reaction_message import ReactionToIncomingMessage, SendMessage
from shared.xml_classes.common_messages import PowerDeliveryReq, MessageHeaderType, ChargeProgressType, ProcessingType
from shared.xml_classes.dc import MessageHeaderType as DcMessageHeaderType
import time
from shared.xml_classes.dc import DcPreChargeReq


class WaitForDcPreChargeResponse(DcEVState):
    def __init__(self):
        super(WaitForDcPreChargeResponse, self).__init__(name="WaitForDcPreChargeRes")
        self.processed = False

    def process_payload(self, payload) -> ReactionToIncomingMessage:
        extra_data = {}
        reaction = SendMessage()
        if self.processed:
            request = PowerDeliveryReq()
            request.header = MessageHeaderType(self.session_parameters.session_id, int(time.time()))
            request.charge_progress = ChargeProgressType.START
            request.evprocessing = ProcessingType.FINISHED
            self.session_parameters.processing = False
            reaction.msg_type = "Common"
        else:
            request = DcPreChargeReq()
            request.header = DcMessageHeaderType(self.session_parameters.session_id, int(time.time()))
            present_voltage = self.controller.data_model.evpresent_voltage  # TODO: handle error when this is not
            # initialized
            evsepresent_voltage = payload.evsepresent_voltage
            if evsepresent_voltage != present_voltage:
                request.evprocessing = ProcessingType.ONGOING
            else:
                request.evprocessing = ProcessingType.FINISHED
                self.processed = True
            self.controller.data_model.evpresent_voltage = evsepresent_voltage
            request.evtarget_voltage = self.controller.data_model.evpresent_voltage
            request.evpresent_voltage = self.controller.data_model.evpresent_voltage
            reaction.msg_type = "DC"

        reaction.message = request
        reaction.extra_data = extra_data
        return reaction
