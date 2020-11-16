from math import sqrt

from voronoi import Polygon, Point, Coordinate
from voronoi.graph import Vertex
import numpy as np
from voronoi.visualization import visualize


class BoundingCircle(Polygon):

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.polygon_vertices = []
        self.center = Coordinate(self.x, self.y)
        self.max_x = self.x + self.radius
        self.min_x = self.x - self.radius
        self.max_y = self.y + self.radius
        self.min_y = self.y - self.radius

    def inside(self, point):
        return (self.x - point.x)**2 + (self.y - point.y)**2 < self.radius**2

    def finish_edges(self, edges, vertices, points, event_queue, verbose=False):
        resulting_edges = []
        for edge in edges:
            A = edge.get_origin()
            B = edge.twin.get_origin()

            if A is None or not self.inside(A):
                self.trim_edge(edge)

            if B is None or not self.inside(B):
                self.trim_edge(edge.twin)

            resulting_edges.append(edge)

            visualize(y=-1000, current_event="nothing", bounding_poly=self,
                      points=points, vertices=vertices + self.polygon_vertices, edges=edges, arc_list=[], event_queue=event_queue)

        # Re-order polygon vertices
        self.polygon_vertices = self.get_ordered_vertices(self.polygon_vertices)

        return resulting_edges, self.polygon_vertices


    def trim_edge(self, edge, twisted=False):
        if edge.get_origin() is None or edge.twin.get_origin() is None:
            point = self.cut_ray(edge, twisted)
        else:
            point = self.cut_line(edge)

        # Create vertex
        v = Vertex(point=point)
        v.incident_edges.append(edge)
        edge.origin = v
        self.polygon_vertices.append(v)

        return edge

    def get_ray(self, edge):
        A = edge.origin.breakpoint[0]
        B = edge.origin.breakpoint[1]
        center = Point(x=(A.x+B.x)/2., y=(A.y+B.y)/2.)

        if edge.twin.get_origin() is None:
            ray_start = center
        else:
            ray_start = edge.twin.origin.point
        a = (B.x - A.x) / (B.y - A.y)
        c = center.x * a + center.y
        return ray_start, center, a, c

    def cut_line(self, edge):
        A = edge.get_origin()
        B = edge.twin.get_origin()
        a = - (B.y - A.y) / (B.x - A.x)
        c = (A.y * B.x - B.y * A.x) / (B.x - A.x)
        point1, point2 = self.cut(a,c)
        dx = (A.x - B.x)
        dy = (A.y - B.y)
        dpx = (A.x - point1.x)
        dpy = (A.y - point1.y)
        if abs((dpx * dx + dpy * dy)/sqrt(dx**2 + dy**2)/sqrt(dpx**2 + dpy**2)-1.) < 1e-5 :
            return point1
        else:
            return point2

    def cut_ray(self, edge, twisted=False):
        A, B, a, c = self.get_ray(edge)
        point1, point2 = self.cut(a,c)

        dx = (edge.origin.breakpoint[0].x - edge.origin.breakpoint[1].x)
        dy = (edge.origin.breakpoint[0].y - edge.origin.breakpoint[1].y)
        dpx = (edge.origin.breakpoint[0].x - point1.x)
        dpy = (edge.origin.breakpoint[0].y - point1.y)
        if dx * dpy - dy * dpx < 0:
            return point1
        else:
            return point2

    def cut(self, a, c):
        b = 1
        d = c - a * self.x - b * self.y
        a_sq_b_sq = a**2 + b**2
        big_sqrt = sqrt(self.radius**2 * a_sq_b_sq - d**2).real

        x1 = self.x + (a * d + b * big_sqrt)/a_sq_b_sq
        y1 = self.y + (b * d - a * big_sqrt)/a_sq_b_sq
        point1 = Point(x=x1, y=y1)
        x2 = self.x + (a * d - b * big_sqrt)/a_sq_b_sq
        y2 = self.y + (b * d + a * big_sqrt)/a_sq_b_sq
        point2 = Point(x=x2, y=y2)

        return point1, point2
