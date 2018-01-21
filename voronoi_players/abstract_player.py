import abc

from data_structures.types import GameState


class Player(metaclass=abc.ABCMeta):
    """
    A template definition of a player, serving as the contract between different implementations and the game object.
    """

    def __init__(self, player_nr: int, state: GameState):
        self.player_nr = player_nr
        self.state = state

    @abc.abstractmethod
    def place_points(self) -> GameState:
        pass
