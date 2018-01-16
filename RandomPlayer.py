import random

from AbstractPlayer import Player
from data_structures.types import Point


class RandomPlayer(Player):

    @property
    def place_points(self):
        for _ in range(self.state.m if self.player_nr == 1 else self.state.n):
            self.state.points.append(Point(
                random.uniform(0, self.state.width),
                random.uniform(0, self.state.height),
                self.player_nr
            ))
        return self.state
