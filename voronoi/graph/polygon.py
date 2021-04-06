from voronoi.graph import Coordinate, Vertex, HalfEdge
from voronoi.graph.algebra import Algebra
import numpy as np

from voronoi.observers.message import Message
from voronoi.observers.subject import Subject


class Polygon(Subject):
    def __init__(self, tuples):
        super().__init__()
        points = [Coordinate(x, y) for x, y in tuples]
        self.points = points
        min_y = min([p.yd for p in self.points])
        min_x = min([p.xd for p in self.points])
        max_y = max([p.yd for p in self.points])
        max_x = max([p.xd for p in self.points])
        center = Coordinate((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.min_y, self.min_x, self.max_y, self.max_x, self.center = min_y, min_x, max_y, max_x, center

        self.points = self.order_points(self.points)
        self.polygon_vertices = []
        for point in self.points:
            self.polygon_vertices.append(Vertex(point.xd, point.yd))

    def order_points(self, points):
        clockwise = sorted(points, key=lambda point: (-180 - Algebra.calculate_angle(point, self.center)) % 360)
        return clockwise

    def get_ordered_vertices(self, vertices):
        vertices = [vertex for vertex in vertices if vertex.xd is not None]
        clockwise = sorted(vertices,
                           key=lambda vertex: (-180 - Algebra.calculate_angle(vertex, self.center)) % 360)
        return clockwise

    @staticmethod
    def get_closest_point(position, points):
        distances = [Algebra.distance(position, p) for p in points]
        index = np.argmin(distances)
        return points[index]

    def finish_polygon(self, edges, existing_vertices, points):
        vertices = self.get_ordered_vertices(self.polygon_vertices)
        vertices = list(vertices) + [vertices[0]]  # <- The extra vertex added here, should be removed later
        cell = self.get_closest_point(vertices[0], points)
        previous_edge = None
        for index in range(0, len(vertices) - 1):

            # Get origin
            origin = vertices[index]
            end = vertices[index + 1]

            # If vertex is connected to other edges, update the cell
            if len(origin.connected_edges) > 0:
                cell = origin.connected_edges[0].twin.incident_point

            # Create the edge
            edge = HalfEdge(cell, origin=origin, twin=HalfEdge(None, origin=end))
            origin.connected_edges.append(edge)
            end.connected_edges.append(edge.twin)

            # Add first edge if needed
            if cell:
                cell.first_edge = cell.first_edge or edge

            # Connect edges
            if len(end.connected_edges) > 0:
                edge.set_next(end.connected_edges[0])

            # Connect to incoming edge, or previous edge
            if len(origin.connected_edges) > 0:
                origin.connected_edges[0].twin.set_next(edge)
            elif previous_edge is not None:
                previous_edge.set_next(edge)

            # Add the edge to the list
            edges.add(edge)

            # Set previous edge
            previous_edge = edge

        existing_vertices = [i for i in existing_vertices if self.inside(i)]

        return edges, vertices[:-1] + existing_vertices

    def get_coordinates(self):
        return [(i.xd, i.yd) for i in self.points]

    def finish_edges(self, edges, **kwargs):
        resulting_edges = set()
        for edge in edges:

            if edge.get_origin() is None or not self.inside(edge.get_origin()):
                self.finish_edge(edge)

            if edge.twin.get_origin() is None or not self.inside(edge.twin.get_origin()):
                self.finish_edge(edge.twin)

            if edge.get_origin() is not None and edge.twin.get_origin() is not None:
                resulting_edges.add(edge)
            else:
                edge.delete()
                edge.twin.delete()
                self.notify_observers(Message.DEBUG, payload=f"Edges {edge} and {edge.twin} deleted!")

        # Re-order polygon vertices
        self.polygon_vertices = self.get_ordered_vertices(self.polygon_vertices)

        return resulting_edges, list(self.polygon_vertices)

    def finish_edge(self, edge):
        # Sweep line position
        sweep_line = self.min_y - abs(self.max_y)

        # Start should be a breakpoint
        start = edge.get_origin(y=sweep_line, max_y=self.max_y)

        # End should be a vertex
        end = edge.twin.get_origin(y=sweep_line, max_y=self.max_y)

        # Get point of intersection
        point = self.get_intersection_point(end, start)

        # Create vertex
        v = Vertex(point.x, point.y) if point is not None else Vertex(None, None)
        v.connected_edges.append(edge)
        edge.origin = v
        self.polygon_vertices.append(v)

        return edge

    def on_edge(self, point):
        vertices = self.points + self.points[0:1]
        for i in range(0, len(vertices) - 1):
            dxc = point.xd - vertices[i].xd
            dyc = point.yd - vertices[i].yd
            dx1 = vertices[i + 1].xd - vertices[i].xd
            dy1 = vertices[i + 1].yd - vertices[i].yd

            cross = dxc * dy1 - dyc * dx1

            if cross == 0:
                return True
        return False

    def inside(self, point):
        # if self.on_edge(point):
        #     return False

        # Ray-casting algorithm based on
        # http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
        # Javascript implementation from https://github.com/substack/point-in-polygon

        vertices = self.points + self.points[0:1]

        x = point.xd
        y = point.yd
        inside = False

        for i in range(0, len(vertices) - 1):
            j = i + 1
            xi = vertices[i].xd
            yi = vertices[i].yd
            xj = vertices[j].xd
            yj = vertices[j].yd

            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside

        return inside

    def get_intersection_point(self, orig, end):
        p = self.points + [self.points[0]]
        points = []

        point = None

        for i in range(0, len(p) - 1):
            intersection_point = Algebra.get_intersection(orig, end, p[i], p[i + 1])
            if intersection_point:
                points.append(intersection_point)

        if not points:
            return None

        max_distance = Algebra.distance(orig, end)

        # Find the intersection point that is furthest away from the start
        if points:
            distances = [Algebra.distance(orig, p) for p in points]
            distances = [i for i in distances if i <= max_distance]
            if distances:
                point = points[np.argmax(distances)]

        return point
