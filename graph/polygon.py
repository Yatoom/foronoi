from graph import Point, Vertex, HalfEdge
import math
from graph.algebra import Algebra
from nodes import Breakpoint
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
        clockwise = sorted(points, key=lambda point: (-180 - Algebra.calculate_angle(point, self.center)) % 360)
        return clockwise

    def get_ordered_vertices(self, vertices):
        vertices = [vertex for vertex in vertices if vertex.position is not None]
        clockwise = sorted(vertices,
                           key=lambda vertex: (-180 - Algebra.calculate_angle(vertex.position, self.center)) % 360)
        return clockwise

    def finish_polygon(self, edges, existing_vertices, points):
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
        resulting_edges = []
        for edge in edges:

            if edge.get_origin() is None or not self.inside(edge.get_origin()):
                self.finish_edge(edge)

            if edge.twin.get_origin() is None or not self.inside(edge.twin.get_origin()):
                self.finish_edge(edge.twin)

            resulting_edges.append(edge)

        # Handle cases where the first edge of a point is outside the bounding box
        # print("Handle cases")
        # for p in points:
        #     start = p.first_edge
        #     while p.first_edge.get_origin() is None and p.first_edge.next != start:
        #         p.first_edge = p.first_edge.next
        #     if start != p.first_edge:
        #         print("Adapted")
        # print("Handled")

        # Re-order polygon vertices
        self.polygon_vertices = self.get_ordered_vertices(self.polygon_vertices)

        return resulting_edges, self.polygon_vertices

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

        vertices = self.points + self.points[0:1]

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
        p = self.points + [self.points[0]]
        points = []
        for i in range(0, len(p) - 1):
            point = Polygon.check_intersection(p[i], p[i + 1], orig, end)
            if point:
                points.append(point)

        if not points:
            return None
        magnitudes = [Algebra.magnitude(np.array([end.x, end.y]) - np.array([i.x, i.y])) for i in points]
        point = points[np.argmin(magnitudes)]

        return point
        # raise Exception("No intersection point could be found.")

    @staticmethod
    def check_intersection(a, b, c, d):
        """
            Checks if a ray intersects with a line segment, using angles.

            :param a: first point of line segment
            :param b: second point of line segment
            :param c: origin of ray
            :param d: some point along the ray
        """
        return Algebra.get_intersection(orig=c, end=d, p1=a, p2=b)


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

    print(poly.inside(Point(0.7, 6.1)))
