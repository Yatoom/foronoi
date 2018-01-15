""""
A template definition of a player, serving as the contract between different implementations and the game object.
"""

import abc

class AbstractPlayer(metaclass=abc.ABCMeta):
    def some_player_interface(self):
        pass