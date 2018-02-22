from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(4.6, 11.44),
    Point(12.7, 10.6),
    Point(13.9, 6.76),
    Point(8.7, 7.7),
    Point(7.1, 4.24),
]

v = Algorithm(BoundingBox(0, 25, 0, 25))
v.create_diagram(points=points, visualize_steps=True, verbose=True)

for point in v.points:
    print(point.cell_size(2), end=",")