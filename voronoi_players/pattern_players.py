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
            for i in range(nr_points):
                self.state.points.append(Point(
                    (i % points_per_side) * point_interval + 0.5 * point_interval,
                    int(i / points_per_side) * point_interval + 0.5 * point_interval,
                    self.player_nr
                ))
        return self.state


class SquareLongPlayer(Player):
    """
    Concrete player class that places points in a rectangle pattern
    Currently only works if the game board is square and behaves best if the nr of points to place is a square
    """

    @property
    def place_points(self):
        if self.state.width != self.state.height:
            print('The Long Square Player does not work if the game board is not square')
        else:
            nr_points = self.state.m if self.player_nr == 1 else self.state.n
            points_per_side = math.ceil(math.sqrt(nr_points))
            point_interval: float = self.state.width / points_per_side
            for i in range(nr_points):
                y_offset = 0.25 * point_interval * (-1 if int(i / points_per_side) % 2 == 0 else 1)
                self.state.points.append(Point(
                    (i % points_per_side) * point_interval + 0.5 * point_interval,
                    int(i / points_per_side) * point_interval + 0.5 * point_interval + y_offset,
                    self.player_nr
                ))
        return self.state


class TrianglePlayer(Player):
    """
    Concrete player class that places points in a triangle pattern
    Currently only works if the game board is square and behaves best if the nr of points to place is a square
    """

    @property
    def place_points(self):
        if self.state.width != self.state.height:
            print('The Triangle Player does not work if the game board is not square')
        else:
            nr_points = self.state.m if self.player_nr == 1 else self.state.n
            points_per_side = math.ceil(math.sqrt(nr_points))
            point_interval: float = self.state.width / points_per_side
            for i in range(nr_points):
                x_offset = 0.25 * point_interval * (-1 if int(i / points_per_side) % 2 == 0 else 1)
                self.state.points.append(Point(
                    (i % points_per_side) * point_interval + 0.5 * point_interval + x_offset,
                    int(i / points_per_side) * point_interval + 0.5 * point_interval,
                    self.player_nr
                ))
        return self.state


class TriangleLongPlayer(Player):
    """
    Concrete player class that places points in a long triangle pattern
    Currently only works if the game board is square and behaves best if the nr of points to place is a square
    """

    @property
    def place_points(self):
        if self.state.width != self.state.height:
            print('The Long Triangle Player does not work if the game board is not square')
        else:
            nr_points = self.state.m if self.player_nr == 1 else self.state.n
            points_per_side = math.ceil(math.sqrt(nr_points))
            point_interval: float = self.state.width / points_per_side
            for i in range(nr_points):
                x_offset = 0.25 * point_interval * (-1 if int(i / points_per_side) % 2 == 0 else 1)
                y_offset = 0.25 * point_interval * (-1 if int(i / points_per_side) % 2 == 0 else 1)
                self.state.points.append(Point(
                    (i % points_per_side) * point_interval + 0.5 * point_interval + x_offset,
                    int(i / points_per_side) * point_interval + 0.5 * point_interval + y_offset,
                    self.player_nr
                ))
        return self.state


class CirclePlayer(Player):
    """
    Concrete player class that places points in a circle centered on the middle of the game board
    The radius of the circle is min(width,height)/4
    """

    @property
    def place_points(self):
        nr_points = self.state.m if self.player_nr == 1 else self.state.n
        radius = min(self.state.width, self.state.height)/4.0
        radial_interval = 2 * math.pi / nr_points
        for i in range(nr_points):
            self.state.points.append(Point(
                (math.cos(i * radial_interval) * radius) + (self.state.width/2.0),
                (math.sin(i * radial_interval) * radius) + (self.state.height/2.0),
                self.player_nr
            ))
        return self.state


class CircleCenterPlayer(Player):
    """
    Concrete player class that places points in a circle centered on the middle of the game board
    The radius of the circle is min(width,height)/4
    """

    @property
    def place_points(self):
        nr_points = self.state.m if self.player_nr == 1 else self.state.n
        radius = min(self.state.width, self.state.height)/4.0
        radial_interval = 2 * math.pi / (nr_points  - 1)
        self.state.points.append(Point(self.state.width / 2.0, self.state.height / 2.0))
        for i in range(nr_points - 1):
            self.state.points.append(Point(
                (math.cos(i * radial_interval) * radius) + (self.state.width/2.0),
                (math.sin(i * radial_interval) * radius) + (self.state.height/2.0),
                self.player_nr
            ))
        return self.state


class LinePlayer(Player):
    """
    Concrete player class that places points in a horizontal line
    """

    @property
    def place_points(self):
        nr_points = self.state.m if self.player_nr == 1 else self.state.n
        point_interval: float = self.state.width / nr_points
        for i in range(nr_points):
            self.state.points.append(Point(
                (i * point_interval) + (0.5 * point_interval),
                self.state.height / 2.0,
                self.player_nr
            ))
        return self.state
