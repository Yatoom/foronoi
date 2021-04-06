from foronoi.graph import Coordinate, Vertex, HalfEdge
from foronoi.graph.algebra import Algebra
import numpy as np

from foronoi.observers.message import Message
from foronoi.observers.subject import Subject


class Polygon(Subject):
    def __init__(self, tuples):
        """
        A bounding polygon that will clip the edges and fit around the Voronoi diagram.

        Parameters
        ----------
        tuples: (float, float)
            x,y-coordinates of the polygon's vertices
        """

        super().__init__()
        points = [Coordinate(x, y) for x, y in tuples]
        self.points = points
        min_y = min([p.yd for p in self.points])
        min_x = min([p.xd for p in self.points])
        max_y = max([p.yd for p in self.points])
        max_x = max([p.xd for p in self.points])
        center = Coordinate((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.min_y, self.min_x, self.max_y, self.max_x, self.center = min_y, min_x, max_y, max_x, center

        self.points = self._order_points(self.points)
        self.polygon_vertices = []
        for point in self.points:
            self.polygon_vertices.append(Vertex(point.xd, point.yd))

    def _order_points(self, points):
        clockwise = sorted(points, key=lambda point: (-180 - Algebra.calculate_angle(point, self.center)) % 360)
        return clockwise

    def _get_ordered_vertices(self, vertices):
        vertices = [vertex for vertex in vertices if vertex.xd is not None]
        clockwise = sorted(vertices,
                           key=lambda vertex: (-180 - Algebra.calculate_angle(vertex, self.center)) % 360)
        return clockwise

    @staticmethod
    def _get_closest_point(position, points):
        distances = [Algebra.distance(position, p) for p in points]
        index = np.argmin(distances)
        return points[index]

    def finish_polygon(self, edges, existing_vertices, points):
        """
        Creates half-edges on the bounding polygon that link with Voronoi diagram's half-edges and existing vertices.

        Parameters
        ----------
        edges: list(HalfEdge)
            The list of clipped edges from the Voronoi diagram
        existing_vertices: set(Vertex)
            The list of vertices that already exists in the clipped Voronoi diagram, and vertices
        points: set(Point)
            The list of cell points

        Returns
        -------
        edges: list(HalfEdge)
            The list of all edges including the bounding polygon's edges
        vertices: list(Vertex)
            The list of all vertices including the
        """
        vertices = self._get_ordered_vertices(self.polygon_vertices)
        vertices = list(vertices) + [vertices[0]]  # <- The extra vertex added here, should be removed later
        cell = self._get_closest_point(vertices[0], points)
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
            edges.append(edge)

            # Set previous edge
            previous_edge = edge

        existing_vertices = [i for i in existing_vertices if self.inside(i)]

        return edges, vertices[:-1] + existing_vertices

    def get_coordinates(self):
        return [(i.xd, i.yd) for i in self.points]

    def finish_edges(self, edges, **kwargs):
        """
        Clip the edges to the bounding box/polygon, and remove edges and vertices that are fully outside.
        Inserts vertices at the clipped edges' endings.

        Parameters
        ----------
        edges: list(HalfEdge)
            A list of edges in the Voronoi diagram. Every edge should be presented only by one half edge.

        Returns
        -------
        clipped_edges: list(HalfEdge)
            A list of clipped edges
        """
        resulting_edges = list()
        for edge in edges:

            if edge.get_origin() is None or not self.inside(edge.get_origin()):
                self._finish_edge(edge)

            if edge.twin.get_origin() is None or not self.inside(edge.twin.get_origin()):
                self._finish_edge(edge.twin)

            if edge.get_origin() is not None and edge.twin.get_origin() is not None:
                resulting_edges.append(edge)
            else:
                edge.delete()
                edge.twin.delete()
                self.notify_observers(Message.DEBUG, payload=f"Edges {edge} and {edge.twin} deleted!")

        return resulting_edges

    def _finish_edge(self, edge):
        # Sweep line position
        sweep_line = self.min_y - abs(self.max_y)

        # Start should be a breakpoint
        start = edge.get_origin(y=sweep_line, max_y=self.max_y)

        # End should be a vertex
        end = edge.twin.get_origin(y=sweep_line, max_y=self.max_y)

        # Get point of intersection
        point = self._get_intersection_point(end, start)

        # Create vertex
        v = Vertex(point.x, point.y) if point is not None else Vertex(None, None)
        v.connected_edges.append(edge)
        edge.origin = v
        self.polygon_vertices.append(v)

        return edge

    def _on_edge(self, point):
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
        """Tests whether a point is inside a polygon.
        Based on the Javascript implementation from https://github.com/substack/point-in-polygon

        Parameters
        ----------
        point: Point
            The point for which to check if it it is inside the polygon

        Returns
        -------
        inside: bool
            Whether the point is inside or not
        """

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

    def _get_intersection_point(self, orig, end):
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
