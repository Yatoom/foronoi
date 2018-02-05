from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    Point(2, 2.5),
    Point(4, 2.5),
    Point(6, 2.5),
    Point(2, 7.5),
    Point(4, 7.5),
    Point(6, 7.5),
]

v = Algorithm(BoundingBox(0, 8, 0, 10))
v.create_diagram(points=points, visualize_steps=True, verbose=True)