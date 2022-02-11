"""
.. module:: start_evse
   :platform: Unix
   :synopsis: The main script for SECC.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""
import sys
sys.path.append("..")
import asyncio
from evse_session_handler import EVSESessionHandler
from shared.log import logger
from evse_dummy_controller import EVSEDummyController


def start_evse(controller) -> None:
    """Starts the EVSE.

    :param controller: The controller that will handle the data.
    :return:
    """
    logger.info("Starting EVSE.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session_handler = EVSESessionHandler()
    state_machine = controller.state_machine
    asyncio.get_event_loop().run_until_complete(state_machine.unset_pwm())
    while not state_machine.is_B():
        logger.info("Waiting for EV to plug.")
        loop.run_until_complete(state_machine.plug())
        loop.run_until_complete(asyncio.sleep(1))
    session_handler.start_new_session(controller)
    loop.run_forever()


if __name__ == '__main__':
    controller = EVSEDummyController()
    start_evse(controller)
