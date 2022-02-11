"""
.. module:: reaction_message
   :platform: Unix
   :synopsis: A module that describes what the reaction should be when receiving a specific message.

.. Copyright 2022 EDF 

.. moduleauthor:: Oscar RODRIGUEZ INFANTE, Tony ZHOU, Trang PHAM, Efflam OLLIVIER 

.. License:: This source code is licensed under the MIT License.


"""


class ReactionToIncomingMessage:
    """This is a class that contains any useful information about an incoming message and the reaction to it.

    """
    def __init__(self):
        self.__message = None
        self.__extra_data = None

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    @property
    def extra_data(self):
        return self.__extra_data

    @extra_data.setter
    def extra_data(self, data):
        self.__extra_data = data

    @property
    def next_state(self):
        return self.__next_state


class SendMessage(ReactionToIncomingMessage):
    """This is a reaction to a message that tells it to send it. Inherits from ReactionToIncomingMessage.

    """
    def __init__(self):
        super(SendMessage, self).__init__()


class TerminateSession(ReactionToIncomingMessage):
    """This is a reaction to a message that tells it to end the session. Inherits from ReactionToIncomingMessage.

    """
    pass


class ChangeState(ReactionToIncomingMessage):
    """This is a reaction to a message that tells it to change the state. Inherits from ReactionToIncomingMessage. Not
    really used, so consider removing it.

    """
    pass


class PauseSession(ReactionToIncomingMessage):
    """This is a reaction to a message that tells it to pause the session. Inherits from ReactionToIncomingMessage. Not
    really used, to be implemented in later versions.

    """
    pass
