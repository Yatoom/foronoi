from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    Point(1, 1),
    Point(1, 4),
    Point(1, 7),
    Point(1, 10),

    Point(4, 1),
    Point(4, 4),
    Point(4, 7),
    Point(4, 10),

    Point(7, 1),
    Point(7, 4),
    Point(7, 7),
    Point(7, 10),

    Point(10, 1),
    Point(10, 4),
    Point(10, 7),
    Point(10, 10),
]

v = Algorithm(BoundingBox(0, 11, 0, 11))
v.create_diagram(points=points, visualize_steps=False, verbose=True)