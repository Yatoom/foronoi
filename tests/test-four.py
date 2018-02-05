from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    # Points from https://www.desmos.com/calculator/ejatebvup4
    Point(2.5, 2.5),
    Point(2.5, 7.5),
    Point(7.5, 1.5),
    Point(7.5, 7.5),
]

v = Algorithm(BoundingBox(0, 10, 0, 10))
v.create_diagram(points=points, visualize_steps=True, verbose=True)