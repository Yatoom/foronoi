import math

from AbstractPlayer import Player
from fortune_algorithm import Voronoi


def calculatedistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


class EdgePlayer(Player):

    def place_points(self, weight_edge_length, weight_inner_point_distance):

        # Check whether currently player 2 is playing (if not then return error)
        if self.player_nr != 2:
            print('The EDGE-PLAYER STRATEGY only works for Player 2')
        else:
            # Create a list with only points for player 1
            points_player1 = filter((lambda point: point.player == 1), self.state.points)

            # Construct a Voronoi for the points of player 1
            voronoi_player1 = Voronoi.create_diagram(points_player1)

            # Check all edges in Voronoi of player 1
            for edge in voronoi_player1:
                edge_start = edge.origin
                edge_end = edge.next.origin

                inner_point1 = edge.inner_point
                inner_point2 = edge.twin.inner_point

                edge_length = calculatedistance(edge_start.x, edge_start.y,
                                                            edge_end.x, edge_end.y)
                inner_point_distance = calculatedistance(inner_point1.x, inner_point1.y,
                                                            inner_point2.x, inner_point2.y)
                desireabilityOfEdge = weight_edge_length * edge_length \
                                        + weight_inner_point_distance * inner_point_distance
