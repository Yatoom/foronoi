from graph import Point, Vertex, HalfEdge
import math
import numpy as np


class Polygon:
    def __init__(self, points):
        self.points = points
        min_y = min([p.y for p in self.points])
        min_x = min([p.x for p in self.points])
        max_y = max([p.y for p in self.points])
        max_x = max([p.x for p in self.points])
        center = Point((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.min_y, self.min_x, self.max_y, self.max_x, self.center = min_y, min_x, max_y, max_x, center

        self.points = self.order_points(self.points)
        self.polygon_vertices = []
        for point in self.points:
            self.polygon_vertices.append(Vertex(point=point))

        print(self.points)

    def order_points(self, points):
        clockwise = sorted(points, key=lambda point: (-180 - Polygon.calculate_angle(point, self.center)) % 360)
        return clockwise

    def get_ordered_vertices(self, vertices):
        clockwise = sorted(vertices,
                           key=lambda vertex: (-180 - Polygon.calculate_angle(vertex.position, self.center)) % 360)
        return clockwise

    def finish_polygon(self, edges, existing_vertices):
        vertices = self.get_ordered_vertices(self.polygon_vertices)
        vertices = vertices + [vertices[0]]
        cell = None
        previous_edge = None
        for index in range(0, len(vertices) - 1):

            # Get origin
            origin = vertices[index]
            end = vertices[index + 1]

            # If vertex is connected to other edges, update the cell
            if len(origin.incident_edges) > 0:
                cell = origin.incident_edges[0].twin.incident_point

            # Create the edge
            edge = HalfEdge(cell, origin=origin, twin=HalfEdge(None, origin=end))
            origin.incident_edges.append(edge)
            end.incident_edges.append(edge.twin)

            # Connect edges
            if len(end.incident_edges) > 0:
                edge.set_next(end.incident_edges[0])

            # Connect to incoming edge, or previous edge
            if len(origin.incident_edges) > 0:
                origin.incident_edges[0].twin.set_next(edge)
            elif previous_edge is not None:
                previous_edge.set_next(edge)

            # Add the edge to the list
            edges.append(edge)

            # Set previous edge
            previous_edge = edge

        return edges, vertices + existing_vertices

    def get_coordinates(self):
        return [(i.x, i.y) for i in self.points]

    def finish_edges(self, edges):
        for edge in edges:
            if edge.get_origin() is None or not self.inside(edge.get_origin()):
                self.finish_edge(edge)
            if edge.twin.get_origin() is None or not self.inside(edge.twin.get_origin()):
                self.finish_edge(edge.twin)

        for edge in edges:
            if not isinstance(edge.origin, Vertex):
                raise Warning('edge has no vertex')
            if not isinstance(edge.twin.origin, Vertex):
                raise Warning('edge has no vertex')

        return edges, self.polygon_vertices

    def finish_edge(self, edge):
        # Start should be a breakpoint
        start = edge.get_origin(y=self.min_y - self.max_y, max_y=self.max_y)

        # End should be a vertex
        end = edge.twin.get_origin(y=self.min_y - self.max_y, max_y=self.max_y)

        # Get point of intersection
        point = self.get_intersection_point(end, start)

        # Create vertex
        v = Vertex(point=point)
        v.incident_edges.append(edge)
        edge.origin = v
        self.polygon_vertices.append(v)

        return edge

    def inside(self, point):
        # Ray-casting algorithm based on
        # http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
        # Javascript implementation from https://github.com/substack/point-in-polygon

        vertices = self.points

        x = point.x
        y = point.y
        inside = False

        for i in range(0, len(vertices) - 1):
            j = i + 1
            xi = vertices[i].x
            yi = vertices[i].y
            xj = vertices[j].x
            yj = vertices[j].y

            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside

        return inside

    def get_intersection_point(self, orig, end):
        p = self.points
        for i in range(0, len(p) - 1):
            point = Polygon.check_intersection(p[i], p[i + 1], orig, end)
            if point:
                return point
        return Polygon.check_intersection(p[len(p) - 1], p[0], orig, end)

    @staticmethod
    def calculate_angle(point, center):
        dx = point.x - center.x
        dy = point.y - center.y
        return math.degrees(math.atan2(dy, dx)) % 360

    @staticmethod
    def line(p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])
        return A, B, -C

    @staticmethod
    def intersection(L1, L2):
        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return Point(x, y)
        else:
            return False

    @staticmethod
    def check_intersection(a, b, c, d):
        """
        Checks if a ray intersects with a line segment, using angles.

        :param a: first point of line segment
        :param b: second point of line segment
        :param c: origin of ray
        :param d: some point along the ray
        :return: Returns a Point if intersecting, or False otherwise
        """

        # If the point is too close to the edge, we need to move it a little

        angle_a = Polygon.calculate_angle(a, c)
        angle_b = Polygon.calculate_angle(b, c)
        angle_d = Polygon.calculate_angle(d, c)

        # Check which one is the smallest side
        one_side = (angle_a - angle_b) % 360
        other_side = 360 - one_side
        smallest_side = min(one_side, other_side)

        # Calculate lines
        L1 = Polygon.line([a.x, a.y], [b.x, b.y])
        L2 = Polygon.line([c.x, c.y], [d.x, d.y])

        if smallest_side == one_side:
            if angle_b <= angle_d <= angle_a:
                return Polygon.intersection(L1, L2)
        elif angle_a <= angle_d <= angle_b:
            return Polygon.intersection(L1, L2)

        return False


if __name__ == "__main__":
    p = [
        Point(1, 3),
        Point(2, 3),
        Point(3, 2),
        Point(3, 1),
        Point(2, 0),
        Point(1, 0),
        Point(0, 1),
        Point(0, 2),
    ]

    poly = Polygon(p)
    orig = Point(1.5, 1.5)
    end_intersect = Point(1.5, -5)
    end_not_intersect = Point(1.5, 5)

    for i in range(0, len(p) - 1):
        print(poly.check_intersection(p[i], p[i + 1], orig, end_intersect))
