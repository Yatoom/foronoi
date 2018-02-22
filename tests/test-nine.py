from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(1, 1),
    Point(1, 3),
    Point(1, 9),

    Point(3, 1),
    Point(3, 3),
    Point(3, 9),

    Point(9, 1),
    Point(9, 3),
    Point(9, 9)
]

v = Algorithm(BoundingBox(0, 10, 0, 10))
v.create_diagram(points=points, visualize_steps=False, verbose=True)