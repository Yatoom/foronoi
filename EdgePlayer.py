import math

from AbstractPlayer import Player
from fortune_algorithm import Voronoi


from data_structures.types import Point


def calculate_distance(p1, p2):
    dist = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def point_along_edge(p1, p2, fraction_of_distance):
    point_x = (p1.x + p2.x) * fraction_of_distance
    point_y = (p1.y + p2.y) * fraction_of_distance
    return point_x, point_y


class EdgePlayer(Player):

    # Set Default values for EdgePlayer
    weight_edge_length = 1
    weight_inner_point_distance = 1

    def place_points(self):
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
                # Find the start and end node of the edge
                edge_start = edge.origin
                edge_end = edge.next.origin

                # Find the player points corresponding to the edge
                inner_point1 = edge.inner_point
                inner_point2 = edge.twin.inner_point

                # Find Midway-point and Halfway-point for edge
                edge_midpoint = Point()
                edge_halfwaypoint = Point()
                edge_midpoint.x, edge_midpoint.y = point_along_edge(inner_point1, inner_point2)
                edge_halfwaypoint.x, edge_halfwaypoint.y = point_along_edge(edge_start, edge_end)

                # If the midway point is closer to the start of the edge than the halfway-point,
                # then the edge should be reversed
                if calculate_distance(edge_midpoint, edge_start) < calculate_distance(edge_halfwaypoint, edge_start):
                    edge_start, edge_end = edge_end, edge_start
                    inner_point1, inner_point2 = inner_point2, inner_point1

                # Find the length of the edge, and the distance between the corresponding player points
                edge_length = calculate_distance(edge_start, edge_end)
                inner_point_distance = calculate_distance(inner_point1, inner_point2)

                # Calculate the desireability of the edge,
                # and store the edge in a tree if the twin has not already been stored.
                desirability_of_edge = self.weight_edge_length * edge_length \
                    + self.weight_inner_point_distance * inner_point_distance
