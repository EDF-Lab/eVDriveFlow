"""
.. module:: gui
   :platform: Unix
   :synopsis: A module that interfaces the GUI to be used.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from abc import abstractmethod


class GUI:
    @abstractmethod
    def setup_ui(self, main_window) -> None:
        """Sets the UI.

        :param main_window: The window containing all the widgets.
        :return:
        """
        pass

    @abstractmethod
    def retranslate_ui(self, main_window) -> None:
        """Retranslates some texts.

        :param main_window: The window containing all the widgets.
        :return:
        """
        pass

    @abstractmethod
    def update(self):
        """Updates the UI.

        :return:
        """
        pass

    @abstractmethod
    def check_state_box(self):
        """Checks the boxes depending on the current state.

        :return:
        """
        pass

    @abstractmethod
    def connect_signals(self):
        """Connects data to their respective widgets.

        :return:
        """
        pass

    @abstractmethod
    def set_ev_settings(self):
        """Sets EV settings.

        :return:
        """
        pass

    @abstractmethod
    def update_timer(self):
        """Updates the departure time timer.

        :return:
        """
        pass
