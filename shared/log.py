"""
.. module:: logger
   :platform: Unix
   :synopsis: A module that implements a custom logger.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""

import logging


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors,
    source: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output"""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    info_format = "[%(asctime)s] %(levelname)s (%(module)s): %(message)s"
    format = "[%(asctime)s] %(levelname)s (%(module)s): %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + info_format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG) # Change this setting for detailed log
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


# This part is for logging in a file. To use it, you have to uncomment it and comment the respective part for ch.
# fh = logging.FileHandler('../build/ev.log')
# fh.setLevel(logging.INFO)
# fh.setFormatter(CustomFormatter())
# logger.addHandler(fh)
