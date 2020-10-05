# internal modules
from random import randint


class Messenger:

    """ Base messenger class """

    def send_message(self, message):
        if randint(1, 2) == 2:
            raise ValueError("Problem -----------")
        return message
