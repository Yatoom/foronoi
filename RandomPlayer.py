import random

from AbstractPlayer import Player
from data_structures.types import Point


class RandomPlayer(Player):

    @property
    def placepoints(self):
        for _ in range(self.gamestate.m if self.playernr == 1 else self.gamestate.n):
            self.gamestate.points.append(Point(
                random.uniform(0, self.gamestate.width),
                random.uniform(0, self.gamestate.height),
                self.playernr))
        return self.gamestate
