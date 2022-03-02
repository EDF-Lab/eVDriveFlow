"""
.. module:: event_handler
   :platform: Unix
   :synopsis: A module that implements an event_handler.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import asyncio
import sys


class KeyboardListener:
    """Class that listens to the keyboard.

    """
    def __init__(self, callback):
        """Basic constructor.

        :param callback: The function that will be called after receiving a keyboard event.
        """
        self.callback = callback
        self.task = asyncio.create_task(self.job())

    async def job(self):
        await self.callback()
