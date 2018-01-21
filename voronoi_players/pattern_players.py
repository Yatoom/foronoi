import math

from voronoi_players.abstract_player import Player
from data_structures.types import Point


class SquarePlayer(Player):
    """
    Concrete player class that places points in a square pattern
    Currently only works if the game board is square and behaves best if the nr of points to place is a square
    """

    @property
    def place_points(self):
        if self.state.width != self.state.height:
            print('The Square Player does not work if the game board is not square')
        else:
            nr_points = self.state.m if self.player_nr == 1 else self.state.n
            points_per_side = math.ceil(math.sqrt(nr_points))
            point_interval: float = self.state.width / points_per_side
            for i in range(nr_points - 1):
                self.state.points.append(Point(
                    (i % points_per_side) * point_interval + 0.5 * point_interval,
                    int(i / points_per_side) * point_interval + 0.5 * point_interval,
                    self.player_nr
                ))
        return self.state.points


class CirclePlayer(Player):
    """
    Concrete player class that places points in a circle centered on the middle of the game board
    The radius of the circle is min(width,height)/4
    """

    @property
    def place_points(self):
        nr_points = self.state.m if self.player_nr == 1 else self.state.n
        radius = min(self.state.width, self.state.height)/4
        radial_interval = 2 * math.pi / nr_points
        for i in range(nr_points - 1):
            self.state.points.append(Point(
                (math.cos(i * radial_interval) / radius) + (self.state.width/2),
                (math.sin(i * radial_interval) / radius) + (self.state.height/2),
                self.player_nr
            ))
        return self.state.points


class CircleCenterPlayer(Player):
    """
    Concrete player class that places points in a circle centered on the middle of the game board
    The radius of the circle is min(width,height)/4
    """

    @property
    def place_points(self):
        nr_points = self.state.m if self.player_nr == 1 else self.state.n
        radius = min(self.state.width, self.state.height)/4
        radial_interval = 2 * math.pi / nr_points
        self.state.points.append(Point(self.state.width / 2, self.state.height / 2))
        for i in range(nr_points - 2):
            self.state.points.append(Point(
                (math.cos(i * radial_interval) / radius) + (self.state.width/2),
                (math.sin(i * radial_interval) / radius) + (self.state.height/2),
                self.player_nr
            ))
        return self.state.points
