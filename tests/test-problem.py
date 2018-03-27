import random

from algorithm import Algorithm
from graph import Polygon, Point


def test(voronoi_points, polygon_points):
    polygon = Polygon(polygon_points)
    v = Algorithm(polygon)
    v.create_diagram(points=voronoi_points, vis_result=True)

# ---------------------------------------------------------

v_points = [
    # Point(64, 90),
    # Point(62, 68),
    Point(73, 99),
    # Point(37, 29),
    # Point(36, 37),
    # Point(3, 94),
    # Point(52, 28),
    # Point(85, 85),
    # Point(33, 73),
    # Point(31, 48),
]

x = 100
y = 100
n = 10
print_input = True

p_points = [
    Point(0, y),
    Point(x, y),
    Point(x / 2, 0)
]

test(v_points, p_points)

