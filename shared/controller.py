"""
.. module:: controller
   :platform: Unix
   :synopsis: A module that implements the controller for 15118.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from platform import machine
from shared.physical_interface import PhysicalInterface
from dataclasses import dataclass


@dataclass
class ControllerInterface:
    """This is a class that will handle the data coming from the physical level as well as from the GUI.

    """
    data_model: dataclass
    state_machine: PhysicalInterface
    virtual_mode: bool = None
    charge_controller_ip: str = ''



    def __post_init__(self):
        self.set_settings()
        self.set_machine()

    def set_settings(self):
        """Sets virtual mode. If False, it will be using an Charge Controller card.

        :return:
        """
        config = self.get_config()
        self.virtual_mode = config["SETTINGS"].getboolean("virtual_mode")
        self.charge_controller_ip = config["NETWORK"].get("charge_controller_ip")


    def set_machine(self):
        """Configures the 61851 state machine.

        :return:
        """
        pass
