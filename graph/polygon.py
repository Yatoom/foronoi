from graph import Point
import math


class Polygon:
    def __init__(self, points):
        self.points = points

    def inside(self, point):
        # ray-casting algorithm based on
        # http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html

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
            intersection = poly.check_intersection(p[i], p[i + 1], orig, end)
            if intersection:
                return p[i], p[i+1], intersection

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

        prox_a = abs(angle_a - angle_d) / abs(angle_a - angle_b)
        prox_b = abs(angle_b - angle_d) / abs(angle_a - angle_b)

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

    print(poly.get_intersection_edge(orig, end_intersect))

    print(poly.inside(Point(1.5, 1.5)))
    print(poly.inside(Point(5, 5)))