from graph import Point, Vertex
import math


class Polygon:
    def __init__(self, points):
        self.points = points
        self.min_y = min([p.y for p in self.points])
        self.min_x = min([p.x for p in self.points])
        self.max_y = max([p.y for p in self.points])
        self.max_x = max([p.x for p in self.points])

        self.points = self.order_points(self.points)
        self.vertices = []
        for point in self.points:
            self.vertices.append(Vertex(point=point))

        print(self.points)

    def order_points(self, points):
        center = Point(self.max_x - self.min_x, self.max_y - self.min_y)
        counter_clockwise = sorted(points, key=lambda point: -Polygon.calculate_angle(point, center))
        return counter_clockwise

    # def get_ordered_vertices(self):
    #     center = Point(self.max_x - self.min_x, self.max_y - self.min_y)
    #     counter_clockwise = sorted(self.vertices, key=lambda vertex: Polygon.calculate_angle(vertex.position, center))
    #     return counter_clockwise[::-1]

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

        return edges

    def finish_edge(self, edge):
        # Start should be a breakpoint
        start = edge.get_origin(y=self.min_y - self.max_y, max_y=self.max_y)

        # End should be a vertex
        end = edge.twin.get_origin(y=self.min_y - self.max_y, max_y=self.max_y)

        # Get point of intersection
        point = self.get_intersection_edge(end, start)

        # Create vertex
        v = Vertex(point=point)
        v.incident_edges.append(edge)
        edge.origin = v
        self.vertices.append(v)

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

    def get_intersection_edge(self, orig, end):
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
    def check_intersection(a, b, c, d):
        """
        Checks if a ray intersects with a line segment, using angles.

        :param a: first point of line segment
        :param b: second point of line segment
        :param c: origin of ray
        :param d: some point along the ray
        :return: Returns a Point if intersecting, or False otherwise
        """

        angle_a = Polygon.calculate_angle(a, c)
        angle_b = Polygon.calculate_angle(b, c)
        angle_d = Polygon.calculate_angle(d, c)

        # Check which one is the smallest side
        one_side = (angle_a - angle_b) % 360
        other_side = 360 - one_side
        smallest_side = min(one_side, other_side)

        prox_a = 1 - abs(angle_a - angle_d) / abs(angle_a - angle_b)
        prox_b = 1 - abs(angle_b - angle_d) / abs(angle_a - angle_b)

        if smallest_side == one_side:
            if angle_b <= angle_d <= angle_a:
                return Point(prox_a * a.x + prox_b * b.x, prox_a * a.y + prox_b * b.y)
        elif angle_a <= angle_d <= angle_b:
            return Point(prox_a * a.x + prox_b * b.x, prox_a * a.y + prox_b * b.y)

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
