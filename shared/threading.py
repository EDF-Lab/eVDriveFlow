"""
.. module:: threading
   :platform: Unix
   :synopsis: A module that implements threading tools to use a GUI.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

from PyQt5.QtCore import QObject, pyqtSignal
from shared.controller import ControllerInterface


class Worker(QObject):
    """This is a class that will handle a specific task in a thread.

    """
    finished = pyqtSignal()

    def __init__(self, controller: ControllerInterface, callback):
        """Basic constructor.

        :param controller: The controller that will handle the data and the view.
        :param callback: The function that will be called by the the thread.
        """
        self.controller = controller
        self.callback = callback
        super(Worker, self).__init__()

    def run(self):
        self.callback(self.controller)
        self.finished.emit()
