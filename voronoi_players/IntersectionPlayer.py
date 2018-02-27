import math

from algorithm import Algorithm
from graph import BoundingBox, Point
from voronoi_players.abstract_player import Player


def calculate_distance(point_1, point_2):
    dist = math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2)
    return dist


def point_along_edge(point_1, point_2, fraction_of_distance):
    point = Point()
    point.x = point_1.x + ((point_2.x - point_1.x) * fraction_of_distance)
    point.y = point_1.y + ((point_2.y - point_1.y) * fraction_of_distance)
    return point


def point_perpendicular_intersection(point_1, point_2, point_perpendicular):
    point_intersection = Point()
    k = ((point_2.y - point_1.y) * (point_perpendicular.x - point_1.x) -
         (point_2.x - point_1.x) * (point_perpendicular.y - point_1.y)) / \
        (math.pow((point_2.y - point_1.y),2) + math.pow((point_2.x - point_1.x),2))
    point_intersection.x = point_perpendicular.x - k * (point_2.y - point_1.y)
    point_intersection.y = point_perpendicular.y + k * (point_2.x - point_1.x)

    return point_intersection


class IntersectionPlayer(Player):

    # Set Default values for EdgePlayer
    weight_combined_edge_length = 1
    weight_combined_inner_point_distance = 1
    weight_nr_of_edges = 1
    weight_nr_of_incident_points = 1

    @property
    def place_points(self):
        # Check whether currently player 2 is playing (if not then return error)
        if self.player_nr != 2:
            print('The EDGE-PLAYER STRATEGY only works for Player 2')
        else:
            print('testerdetest')
            # Create a list with only points for player 1
            points_player1 = list(filter((lambda point: point.player == 1), self.state.points))

            # Construct a Voronoi for the points of player 1
            voronoi = Algorithm(BoundingBox(0, 25, 0, 25))
            voronoi.create_diagram(points_player1, visualize_steps=False)

            # Check all edges in Voronoi of player 1
            edges_seen = []
            points_desirability = []
            points_desirability_factors = []
            for vertex in voronoi.vertices:
                print('if this doesnt show. there are no vertices in voronoi vertices')

                # Calculate edge length and point distance length
                total_edge_length = 0
                total_incident_point_distance = 0
                nr_of_edges = 0
                nr_of_incident_points = 0

                for edge in vertex.incident_edges:
                    # Add edge length of current edge
                    edge_start = edge.origin.position
                    edge_end = edge.twin.origin.position

                    total_edge_length += calculate_distance(edge_start, edge_end)

                    # If incident point exists, add incident point distance for current edge
                    incident_point = edge.incident_point

                    if not incident_point is None:
                        total_incident_point_distance += calculate_distance(vertex.position, incident_point)
                        nr_of_incident_points += 1

                    # Add edge to nr of edges
                    nr_of_edges += 1

                # Calculate the desirability factors of the intersection
                desirability_factor_avg_edge_length = total_edge_length / nr_of_edges
                desirability_factor_avg_incident_distance = total_incident_point_distance / nr_of_incident_points
                desirability_factor_nr_of_edges = nr_of_edges
                desirability_factor_nr_of_incident_points = nr_of_incident_points

                # Check whether point has not already been added before
                if vertex.position not in [x['point'] for x in points_desirability_factors]:
                    points_desirability_factors.append({'point': vertex.position,
                                'avg edge length': desirability_factor_avg_edge_length,
                                'avg incident distance': desirability_factor_avg_incident_distance,
                                'nr of edges': desirability_factor_nr_of_edges,
                                'nr of incident points': desirability_factor_nr_of_incident_points})

            # Find the Min/Max of each desirability factor
            min_desirability_factor_avg_edge_length = min([x['avg edge length'] for x in points_desirability_factors])
            min_desirability_factor_avg_incident_distance = min(
                [x['avg incident distance'] for x in points_desirability_factors])
            min_desirability_factor_nr_of_edges = min([x['nr of edges'] for x in points_desirability_factors])
            min_desirability_factor_nr_of_incident_points = min(
                [x['nr of incident points'] for x in points_desirability_factors])

            max_desirability_factor_avg_edge_length = max([x['avg edge length'] for x in points_desirability_factors])
            max_desirability_factor_avg_incident_distance = max(
                [x['avg incident distance'] for x in points_desirability_factors])
            max_desirability_factor_nr_of_edges = max([x['nr of edges'] for x in points_desirability_factors])
            max_desirability_factor_nr_of_incident_points = max(
                [x['nr of incident points'] for x in points_desirability_factors])

            if max_desirability_factor_avg_edge_length == min_desirability_factor_avg_edge_length:
                max_desirability_factor_avg_edge_length =+ 1
            if max_desirability_factor_avg_incident_distance == min_desirability_factor_avg_incident_distance:
                max_desirability_factor_avg_incident_distance =+ 1
            if max_desirability_factor_nr_of_edges == min_desirability_factor_nr_of_edges:
                max_desirability_factor_nr_of_edges =+ 1
            if max_desirability_factor_nr_of_incident_points == min_desirability_factor_nr_of_incident_points:
                max_desirability_factor_nr_of_incident_points =+ 1

            # Calculate point desirability
            for point_desirability_factor in points_desirability_factors:
                point = point_desirability_factor.get('point')

                print(max_desirability_factor_nr_of_edges, min_desirability_factor_nr_of_edges)

                desirability_of_point = (((point_desirability_factor.get('avg edge length') - min_desirability_factor_avg_edge_length) /
                                         (max_desirability_factor_avg_edge_length - min_desirability_factor_avg_edge_length))
                                            * self.weight_combined_edge_length) + \
                                        (((point_desirability_factor.get('avg incident distance') - min_desirability_factor_avg_incident_distance) /
                                         ( max_desirability_factor_avg_incident_distance - min_desirability_factor_avg_incident_distance))
                                            * self.weight_combined_inner_point_distance) + \
                                        (((point_desirability_factor.get('nr of edges') - min_desirability_factor_nr_of_edges) /
                                         (max_desirability_factor_nr_of_edges - min_desirability_factor_nr_of_edges))
                                            * self.weight_nr_of_edges) + \
                                        (((point_desirability_factor.get('nr of incident points') - min_desirability_factor_nr_of_incident_points) /
                                         (max_desirability_factor_nr_of_incident_points - min_desirability_factor_nr_of_incident_points))
                                            * self.weight_nr_of_incident_points)

                print(point)

                # Store point in points_desirability
                points_desirability.append({'point': point, 'desirability': desirability_of_point})

            # Sort list of points based on their desirability
            points_desirability_sorted = sorted(points_desirability, key=lambda item: item['desirability'], reverse=True)

            print('Desirability: ' + str( points_desirability_sorted))
            print('Point Previous Player: ' + str(self.state.points))

            # Store points for player 2
            for i in range(self.state.m if self.player_nr == 1 else self.state.n):

                self.state.points.append(Point(points_desirability_sorted[i].get('point').x,
                                               points_desirability_sorted[i].get('point').y,
                                               self.player_nr))

            print('Points after Addition: ' + str(self.state.points))
        return self.state
