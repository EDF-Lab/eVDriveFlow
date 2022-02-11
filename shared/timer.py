"""
.. module:: timer
   :platform: Unix
   :synopsis: A module that implements a custom timer class.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import time
from shared.log import logger
import asyncio


class Timer:
    """This is timer implementation that will call a function once its timeout has been reached.

    """
    def __init__(self, timeout: int, callback):
        """Basic constructor for Timer.

        :param timeout: The timeout value.
        :param callback: The callback function that will be called when timing out.

        """
        self.__timeout = timeout
        self.callback = callback
        self.task = None
        self.start_time = None

    async def job(self):
        """Calls callback asynchronously after timeout.

        :return:
        """
        await asyncio.sleep(self.__timeout)
        await self.callback()

    def start(self):
        """Starts Timer.

        :return:
        """
        self.task = asyncio.create_task(self.job())
        self.start_time = time.perf_counter()

    def cancel(self):
        """Cancels Timer.

        :return:
        """
        if not self.task.cancelled():
            self.task.cancel()
        self._get_elapsed_time()

    def _get_elapsed_time(self):
        now = time.perf_counter()
        elapsed_time = now - self.start_time
        self.start_time = now
        return elapsed_time

    @property
    def timeout(self):
        return self.__timeout


class SequenceTimer(Timer):
    """Sequence timer as specified in the standard. Inherits from Timer class.

    """
    def __init__(self, timeout):
        super(SequenceTimer, self).__init__(timeout, self.performance_timeout_callback)

    async def performance_timeout_callback(self):
        """Callback for SequenceTimer.

        :return:
        """
        logger.warning("Sequence timer requirement not fulfilled: over {:0.2f} seconds).".format(self.timeout))


class MessageTimer(Timer):
    """Message timer as specified in the standard. Inherits from Timer class.

    """
    def __init__(self, timeout):
        super(MessageTimer, self).__init__(timeout, self.message_timeout_callback)

    async def message_timeout_callback(self):
        """Callback for MessageTimer.

        :return:
        """
        logger.warning("Message timer requirement not fulfilled: over {:0.2f} seconds).".format(self.timeout))
