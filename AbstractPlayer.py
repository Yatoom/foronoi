""""
A template definition of a player, serving as the contract between different implementations and the game object.
"""

import abc


class Player(metaclass=abc.ABCMeta):
    def __init__(self, playernr, gamestate):
        self.playernr = playernr
        self.gamestate = gamestate

    @abc.abstractmethod
    def placepoints(self):
        pass
