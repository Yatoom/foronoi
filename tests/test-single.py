import random

from algorithm import Algorithm
from graph import Polygon, Point


def test(voronoi_points, polygon_points):
    polygon = Polygon(polygon_points)
    v = Algorithm(polygon)
    v.create_diagram(points=voronoi_points, vis_result=True)


# ---------------------------------------------------------

v_points = [
    Point(50, 50)
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
