"""
.. module:: charge_controller_interface
   :platform: Unix
   :synopsis: A module that allows support for Charge Controller cards.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from shared.physical_interface import PhysicalInterface
import asyncio
from shared.charge_controller_tcp_driver.charge_controller_tcp_client_helper import ChargeControllerTCPClientHelper
from shared.log import logger


class ChargeControllerInterface(PhysicalInterface):
    """This is the class that will interface with the card driver. Inherits from PhysicalInterface.

    """
    def __init__(self, ip_address: str, port: int, machine_type: str):
        self.__helper = ChargeControllerTCPClientHelper(ip_address, port)
        super(ChargeControllerInterface, self).__init__(machine_type)

    async def update_pwm(self):
        while True:
            self.pwm = self.get_pwm()
            await asyncio.sleep(1)

    def get_ev_state(self):
        self.notification_type = "61851"
        self.notify()
        return self.__helper.get_ev_state()

    def set_ev_state(self, state):
        self.__helper.set_ev_state(state)
        self.notification_type = "61851"
        self.notify()
        logger.info("61851 state set to %s.", state)

    def get_pwm(self):
        return self.__helper.get_pwm()

    def is_state_a(self):
        return self.get_ev_state() == 'A'

    def is_state_b(self):
        real_state = self.get_ev_state()
        logger.info("Real state: %s.", real_state)
        return real_state == 'B'

    def is_state_c(self):
        real_state = self.get_ev_state()
        logger.info("Real state: %s.", real_state)
        return real_state == 'C'

    def is_state_e(self):
        real_state = self.get_ev_state()
        logger.info("Real state: %s.", real_state)
        return real_state == 'E'

    async def set_pwm(self):
        self.__helper.set_pwm(5)

    async def unset_pwm(self):
        self.__helper.set_pwm(100)

    def pwm_on(self):
        return 3 <= self.get_pwm() <= 7
