"""
.. module:: start_ev
   :platform: Unix
   :synopsis: A module that instantiates an EV.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""
import sys
sys.path.append("..")
from evcc.ev_session_handler import EVSessionHandler
from shared.log import logger
from evcc.ev_dummy_controller import EVDummyController
import asyncio
import time


def start_ev(controller) -> None:
    """Starts an EV session.

    :param controller: The controller that will handle the data.
    :return:
    """
    logger.info("Starting EV.")
    loop = asyncio.new_event_loop()
    print("Init event loop: ", loop)
    asyncio.set_event_loop(loop)
    session_handler = EVSessionHandler()
    state_machine = controller.state_machine
    while not state_machine.is_B():
        asyncio.get_event_loop().run_until_complete(state_machine.plug())
        logger.info("Waiting for EV to plug. ")
    while not state_machine.pwm_on():
        logger.info("Duty cycle is different from 5%.")
        if controller.virtual_mode:
            asyncio.get_event_loop().run_until_complete(state_machine.set_pwm())
    try:
        session_handler.start_new_session(controller)
    except RuntimeError as err:
        # This is a temporary bug fix to increase the stability of the launch.
        logger.error("Run time error: ", err)
        time.sleep(3)
        start_ev(controller)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    controller = EVDummyController()
    start_ev(controller)
