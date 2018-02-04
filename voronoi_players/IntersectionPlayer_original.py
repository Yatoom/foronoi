import math

from voronoi_players.abstract_player import Player
from algorithm import Algorithm


from data_structures.types import Point


def calculate_distance(p1, p2):
    dist = math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)
    return dist


def point_along_edge(p1, p2, fraction_of_distance):
    point = Point()
    point.x = p1.x + ((p2.x - p1.x) * fraction_of_distance)
    point.y = p1.y + ((p2.y - p1.y) * fraction_of_distance)
    return point


class IntersectionPlayer(Player):

    # Set Default values for EdgePlayer
    weight_combined_edge_length = 1
    weight_combined_inner_point_distance = 1
    weight_nr_of_edges = 1

    @property
    def place_points(self):
        # Check whether currently player 2 is playing (if not then return error)
        print('test3')
        if self.player_nr != 2:
            print('The EDGE-PLAYER STRATEGY only works for Player 2')
        else:
            print('test2')
            # Create a list with only points for player 1
            points_player1 = list(filter((lambda point: point.player == 1), self.state.points))

            # Construct a Voronoi for the points of player 1
            voronoi = Algorithm()
            voronoi_player1 = voronoi.create_diagram(points_player1)

            # Check all intersections in Voronoi of player 1
            half_edges_seen = []
            points_desirability = []
            for half_edge in voronoi.edges:
                # Check whether half edge's twin has already been seen before
                if half_edge not in half_edges_seen:
                    # Find the intersection for the current half edge
                    intersection = half_edge.origin

                    # Find all half edges corresponding to the current intersection
                    half_edges_intersection = []
                    half_edges_intersection.append(half_edge)
                    half_edge_followup = half_edge.twin.next
                    while half_edge_followup != half_edge:
                        half_edges_intersection.append(half_edge_followup)
                        half_edge_followup = half_edge_followup.twin.next

                    # Count the number of edges adjacent to the intersection
                    nr_of_edges = len(half_edges_intersection)

                    # Calculate the edge length adjacent to the intersection
                    edge_length = 0
                    for item in half_edges_intersection:
                        edge_length = edge_length + calculate_distance(item.origin, item.twin.origin)

                    # Calculate the edge length adjacent to the intersection
                    inner_point_distance = 0
                    for item in half_edges_intersection:
                        inner_point_distance = inner_point_distance \
                                               + calculate_distance(item.inner_point, item.twin.inner_point)

                    # Calculate the desirability of the intersection
                    desirability_of_point = self.weight_combined_edge_length * edge_length \
                                            + self.weight_combined_inner_point_distance * inner_point_distance \
                                            + self.weight_nr_of_edges * nr_of_edges

                    # Calculate Point Placement
                    point_placement = intersection
                    point_placement.player = 2

                    # Store point in points_desirability
                    points_desirability.append({'point': point_placement, 'desirability': desirability_of_point})

                    # insert edges for intersection in list of seen edges.
                    half_edges_seen.extend(half_edges_intersection)

            # Sort list of points based on their desirability
            points_desirability_sorted = sorted(points_desirability, key=lambda item: item['desirability'])

            # Store points for player 2
            print(points_desirability_sorted or 'nope')
            for i in range(self.state.n):
                self.state.points.append(points_desirability_sorted[i].get('point'))
        return self.state
