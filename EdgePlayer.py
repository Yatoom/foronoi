import math

from AbstractPlayer import Player
from fortune_algorithm import Voronoi


from data_structures.types import Point


def calculate_distance(p1, p2):
    dist = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def point_along_edge(p1, p2, fraction_of_distance):
    point = Point()
    point.x = p1.x + ((p2.x - p1.x) * fraction_of_distance)
    point.y = p1.y + ((p2.y - p1.y) * fraction_of_distance)
    return point


class EdgePlayer(Player):

    # Set Default values for EdgePlayer
    weight_edge_length = 1
    weight_inner_point_distance = 1
    fraction_between_player_points = 0.0    # Between -1 and 1
    fraction_between_edge_nodes = 0.0       # Between -1 and 1

    def place_points(self):
        # Check whether currently player 2 is playing (if not then return error)
        if self.player_nr != 2:
            print('The EDGE-PLAYER STRATEGY only works for Player 2')
        else:
            # Create a list with only points for player 1
            points_player1 = list(filter((lambda point: point.player == 1), self.state.points))

            # Construct a Voronoi for the points of player 1
            voronoi = Voronoi()
            voronoi_player1 = voronoi.create_diagram(points_player1)

            # Check all edges in Voronoi of player 1
            edges_seen = []
            points_desirability = []
            for half_edge in voronoi_player1:
                # Check whether halfedge's twin has already been seen before
                if half_edge not in edges_seen:
                    edge = half_edge

                    # Find the start and end node of the edge
                    edge_start = edge.origin
                    edge_end = edge.next.origin

                    # Find the player points corresponding to the edge
                    inner_point1 = edge.inner_point
                    inner_point2 = edge.twin.inner_point

                    # Find Midway-point and Halfway-point for edge
                    edge_midpoint = point_along_edge(inner_point1, inner_point2, 0.5)
                    edge_halfwaypoint = point_along_edge(edge_start, edge_end, 0.5)

                    # If the midway point is closer to the start of the edge than the halfway-point,
                    # then the edge should be reversed
                    if calculate_distance(edge_midpoint, edge_start) \
                            < calculate_distance(edge_halfwaypoint, edge_start):
                        edge_start, edge_end = edge_end, edge_start
                        inner_point1, inner_point2 = inner_point2, inner_point1

                    # Find the length of the edge, and the distance between the corresponding player points
                    edge_length = calculate_distance(edge_start, edge_end)
                    inner_point_distance = calculate_distance(inner_point1, inner_point2)

                    # Calculate the desirability of the edge
                    desirability_of_point = self.weight_edge_length * edge_length \
                        + self.weight_inner_point_distance * inner_point_distance

                    # Calculate Point Placement
                    if self.fraction_between_player_points > 0:
                        inner_point = inner_point1
                    else:
                        inner_point = inner_point2
                    if self.fraction_between_player_points > 0:
                        edge_point = edge_end
                    else:
                        edge_point = edge_start
                    point_placement = point_along_edge(
                            edge_point,
                            point_along_edge(edge_halfwaypoint, inner_point, abs(self.fraction_between_player_points)),
                            abs(self.fraction_between_edge_nodes))
                    point_placement.player = 2

                    # Store point in points_desirability
                    points_desirability.append({'point': point_placement, 'desirability': desirability_of_point})

                    # insert edge and edge's twin in list of seen edges.
                    edges_seen.append(edge)
                    edges_seen.append(edge.twin)

            # Sort list of points based on their desirability
            points_desirability_sorted = sorted(points_desirability, key=lambda item: item['desirability'])

            # Store points for player 2
            for i in range(self.state.m if self.player_nr == 1 else self.state.n):
                self.state.points.append(points_desirability_sorted[i].get('point'))
            return self.state
