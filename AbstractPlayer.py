""""
A template definition of a player, serving as the contract between different implementations and the game object.
"""
import abc

from data_structures.types import GameState


class Player(metaclass=abc.ABCMeta):
    def __init__(self, playernr: int, gamestate: GameState):
        self.playernr = playernr
        self.gamestate = gamestate

    @abc.abstractmethod
    def placepoints(self) -> GameState:
        pass
