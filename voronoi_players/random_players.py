import random

from graph import Point
from voronoi_players.abstract_player import Player


class UniformPlayer(Player):
    """
    Concrete player class that places points randomly
    Random is determined by uniform distribution based pseudo-random numbers
    """

    @property
    def place_points(self):
        for _ in range(self.state.m if self.player_nr == 1 else self.state.n):
            self.state.points.append(Point(
                random.uniform(0, self.state.width),
                random.uniform(0, self.state.height),
                self.player_nr
            ))
        return self.state


class NormalPlayer(Player):
    """
    Concrete player class that places points randomly
    Random is determined by normal distribution based pseudo-random numbers
    The mean will be the center of the game board
    """

    # TODO: Implement the normal distribution
    @property
    def place_points(self):
        for _ in range(self.state.m if self.player_nr == 1 else self.state.n):
            self.state.points.append(Point(
                random.uniform(0, self.state.width),
                random.uniform(0, self.state.height),
                self.player_nr
            ))
        return self.state