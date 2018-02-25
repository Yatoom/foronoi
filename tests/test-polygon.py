from algorithm import Algorithm
from graph import Polygon, Point

points = [
    Point(2.5, 2.5),
    Point(4, 7.5),
    Point(7.5, 2.5),
    Point(6, 7.5),
    Point(4, 4),
    Point(3, 3),
    Point(6, 3),
]

polygon_points = [
    Point(2.5, 10),
    Point(5, 10),
    Point(10, 5),
    Point(10, 2.5),
    Point(5, 0),
    Point(2.5, 0),
    Point(0, 2.5),
    Point(0, 5),
]

v = Algorithm(Polygon(polygon_points))
v.create_diagram(points=points, visualize_steps=False, verbose=False)