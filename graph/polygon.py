from graph import Point
import numpy as np
import math
from sklearn.preprocessing import normalize


class Polygon:
    def __init__(self, points):
        self.points = points

    @staticmethod
    def calculate_angle(point, center):
        dx = point.x - center.x
        dy = point.y - center.y
        return math.degrees(math.atan2(dy, dx)) % 360

    @staticmethod
    def is_intersecting(a, b, c, d):
        """
        Checks if a ray intersects with a line segment, using angles.

        :param a: first point of line segment
        :param b: second point of line segment
        :param c: origin of ray
        :param d: some point along the ray
        :return:
        """

        angle_a = Polygon.calculate_angle(a, c)
        angle_b = Polygon.calculate_angle(b, c)
        angle_d = Polygon.calculate_angle(d, c)

        # Check which one is the smallest side
        one_side = (angle_a - angle_b) % 360
        other_side = 360 - one_side
        smallest_side = min(one_side, other_side)

        if smallest_side == one_side:
            if angle_b <= angle_d <= angle_a:
                return True
        elif angle_a <= angle_d <= angle_b:
            return True

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
    end_intersect = Point(5, 5)
    end_not_intersect = Point(2, 2)

    for i in range(0, len(p) - 1):
        print(poly.is_intersecting(p[i], p[i + 1], orig, end_intersect))
