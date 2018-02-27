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

    print(point_1)
    print(point_2)
    print(point_perpendicular.x, point_perpendicular.y)


    k = ((point_2.y - point_1.y) * (point_perpendicular.x - point_1.x) -
         (point_2.x - point_1.x) * (point_perpendicular.y - point_1.y)) / \
        (math.pow((point_2.y - point_1.y),2) + math.pow((point_2.x - point_1.x),2))
    point_intersection.x = point_perpendicular.x - k * (point_2.y - point_1.y)
    point_intersection.y = point_perpendicular.y + k * (point_2.x - point_1.x)

    return point_intersection


class EdgePlayer(Player):

    # Set Default values for EdgePlayer
    weight_edge_length = 1
    weight_inner_point_distance = 1
    fraction_between_player_points = 0.25    # Between -1 and 1
    fraction_between_edge_nodes = 0.00       # Between -1 and 1

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
            for half_edge in voronoi.edges:
                print('if this doesnt show. there are no edges in voronoi edges')
                # Check whether halfedge's twin has already been seen before
                if half_edge not in edges_seen:
                    print('test')

                    edge = half_edge

                    # Determine which edge is A and which is B
                    if not edge.incident_point is None:
                        half_edge_A = edge
                        half_edge_B = edge.twin
                        if edge.twin.incident_point is None:
                            print('A')
                            boundary_edge = True
                        else:
                            print('B')
                            boundary_edge = False
                    else:
                        print('C')
                        half_edge_A = edge.twin
                        half_edge_B = edge
                        boundary_edge = True

                    # Find the coordinates of the start and end point of the edge, in the direction of edge A
                    edge_start = half_edge_A.origin.position
                    edge_end = half_edge_A.twin.origin.position
                    incident_point = half_edge_A.incident_point
                    twin_incident_point = half_edge_A.twin.incident_point

                    # Check whether edge length is greater than 0
                    if calculate_distance(edge_start, edge_end) > 0:
                        # Find midway and halfway-point for edge
                        edge_halfwaypoint = point_along_edge(edge_start, edge_end, 0.5)
                        edge_midpoint = point_perpendicular_intersection(edge_start, edge_end, incident_point)

                        # If both half-edges (A and B) of edge have incident points, check to make sure that
                        #   edge_halfwaypoint comes before edge_midpoint with regards from the direction of edge A.
                        # If this does not hold, swap A and B.
                        if not boundary_edge:
                            if calculate_distance(edge_midpoint, edge_start) \
                                    < calculate_distance(edge_halfwaypoint, edge_start):
                                half_edge_A, half_edge_B = half_edge_B, half_edge_A
                                edge_start, edge_end = edge_end, edge_start
                                incident_point, twin_incident_point = twin_incident_point, incident_point

                        # Find the length of the edge, and the distance between the corresponding player points
                        edge_length = calculate_distance(edge_start, edge_end)
                        inner_point_distance = 2 * calculate_distance(incident_point, edge_midpoint)

                        # If there exists no incident-point for the twin edge, take the absolute value of
                        #   self.fraction_between_player_points
                        if boundary_edge:
                            self.fraction_between_player_points = math.fabs(self.fraction_between_player_points)

                        # Calculate Point Placement
                        if self.fraction_between_player_points >= 0:
                            calculate_location_incident_point = incident_point
                        else:
                            calculate_location_incident_point = twin_incident_point

                        if self.fraction_between_player_points >= 0:
                            calculate_location_vertex_point = edge_start
                        else:
                            calculate_location_vertex_point = edge_end

                        # Calculate point placement
                        point_placement = point_along_edge(
                            point_along_edge(edge_halfwaypoint, calculate_location_incident_point,
                                             math.fabs(self.fraction_between_player_points)),
                            calculate_location_vertex_point,
                            math.fabs(self.fraction_between_edge_nodes))
                        point_placement.player = 2

                        # Check whether point has not already been added before
                        if point_placement not in [x['point'] for x in points_desirability_factors]:
                            points_desirability_factors.append({'point': point_placement,
                                                                'edge length': edge_length,
                                                                'incident distance': inner_point_distance})

                        # insert edge and edge's twin in list of seen edges.
                        edges_seen.append(edge)
                        edges_seen.append(edge.twin)

            # Find the Min/Max of each desirability factor
            min_desirability_factor_avg_edge_length = min(
                [x['edge length'] for x in points_desirability_factors])
            min_desirability_factor_avg_incident_distance = min(
                [x['incident distance'] for x in points_desirability_factors])

            max_desirability_factor_avg_edge_length = max(
                [x['edge length'] for x in points_desirability_factors])
            max_desirability_factor_avg_incident_distance = max(
                [x['incident distance'] for x in points_desirability_factors])

            if max_desirability_factor_avg_edge_length == min_desirability_factor_avg_edge_length:
                max_desirability_factor_avg_edge_length = + 1
            if max_desirability_factor_avg_incident_distance == min_desirability_factor_avg_incident_distance:
                max_desirability_factor_avg_incident_distance = + 1

            # Calculate point desirability
            for point_desirability_factor in points_desirability_factors:
                point = point_desirability_factor.get('point')

                desirability_of_point = (((point_desirability_factor.get('edge length') - min_desirability_factor_avg_edge_length) /
                                          (
                                                      max_desirability_factor_avg_edge_length - min_desirability_factor_avg_edge_length))
                                         * self.weight_edge_length) + \
                                        (((point_desirability_factor.get(
                                            'incident distance') - min_desirability_factor_avg_incident_distance) /
                                          (
                                                      max_desirability_factor_avg_incident_distance - min_desirability_factor_avg_incident_distance))
                                         * self.weight_inner_point_distance)

                print(point)

                # Store point in points_desirability
                points_desirability.append({'point': point, 'desirability': desirability_of_point})

            # Sort list of points based on their desirability
            points_desirability_sorted = sorted(points_desirability, key=lambda item: item['desirability'], reverse=True)

            print('Desirability: ' + str(points_desirability_sorted))
            print('Point Previous Player: ' + str(self.state.points))

            # Store points for player 2
            for i in range(self.state.m if self.player_nr == 1 else self.state.n):
                self.state.points.append(points_desirability_sorted[i].get('point'))

            print('Points after Addition: ' + str(self.state.points))
        return self.state
