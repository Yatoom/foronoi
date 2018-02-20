from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    Point(2.5, 2),
    Point(2.5, 4),
    Point(2.5, 6),
    Point(7.5, 2),
    Point(7.5, 4),
    Point(7.5, 6),
]

v = Algorithm(BoundingBox(0, 10, 0, 8))
v.create_diagram(points=points, visualize_steps=False, verbose=True)