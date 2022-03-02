"""
.. module:: physical_interface
   :platform: Unix
   :synopsis: A module that describes a virtual 61851 interface.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from transitions.extensions.asyncio import AsyncMachine
from shared.log import logger


class PhysicalInterface(AsyncMachine):
    """This is a state machine class that will simulate the changes at a physical level.

    """
    def __init__(self, machine_type : str):
        self.notification_type = "61851"
        self.__pwm = 100
        a_state = "A"
        b_state = "B"
        c_state = "C"
        e_state = "E"
        if machine_type == "ev":
            self.state = e_state
        elif machine_type == "evse":
            self.state = a_state
        else:
            raise "Unknown machine type: " + str(machine_type)
        
        states = [a_state, b_state, c_state, e_state]
        self._observers = []
        super(PhysicalInterface, self).__init__(states=states, initial=self.state)
        # Initial physical state
        if machine_type == "ev":
            self.set_ev_state("B")
        elif machine_type == "evse":
            self.set_ev_state("A")
        else:
            raise "Unknown machine type: " + str(machine_type)

    @property
    def pwm(self):
        logger.info("Current duty cycle is %s.", self.__pwm)
        return self.__pwm

    @pwm.setter
    def pwm(self, value):
        self.__pwm = value
        logger.info("Duty cycle set to %s.", self.__pwm)

    def pwm_on(self):
        """Only two levels of pwm are handled (PWM equals 5% or 100%). Therfore this function is named this way. It
        returns True when pwm value is between 3 and 7.

        :return: bool -- if pwm value is between 3 and 7.
        """
        return 3 <= self.pwm <= 7

    async def set_pwm(self):
        """Only two levels of pwm are handled. Therefore this function is named this way. Sets
        pwm to 5 percent.

        :return:
        """
        self.pwm = 5

    async def unset_pwm(self):
        """Only two levels of pwm are handled. Therefore this function is named this way. Sets
        pwm to 100.

        :return:
        """
        self.pwm = 100

    def get_ev_state(self):
        self.notification_type = "61851"
        self.notify()
        return self.state

    def set_ev_state(self, value):
        self.state = value
        self.notification_type = "61851"
        self.notify()
        logger.info("61851 state set to %s.", self.state)

    async def set_a(self):
        """Sets EV state to state A, 
            this means open circuit between CP and PE

        :return:
        """
        self.set_ev_state("A")

    async def set_b(self):
        """Sets EV state to B, Default/Initial position 
            resistance between CP and PE = 2.7 K Ohms
            
        :return:
        """
        self.set_ev_state("B")

    async def set_c(self):
        """Sets EV state to C, EV Ready position 
            resistance between CP and PE = 882 Ohms

        :return:
        """
        self.set_ev_state("C")

    def is_state_a(self):
        return self.state == 'A'

    def is_state_b(self):
        return self.state == 'B'

    def is_state_c(self):
        return self.state == "C"

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


if __name__ == '__main__':
    machine = PhysicalInterface()
    print(machine.state)
