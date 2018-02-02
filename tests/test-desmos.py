from algorithm import Algorithm
from nodes.point import Point

points = [
    # Points from https://www.desmos.com/calculator/ejatebvup4
    Point(4.6, 11.44),
    # Point(7.3, 11.44),
    Point(12.7, 10.6),
    Point(8.7, 7.7),
    Point(13.9, 6.76),
    Point(7.1, 4.24),
]

v = Algorithm()
v.create_diagram(points=points)