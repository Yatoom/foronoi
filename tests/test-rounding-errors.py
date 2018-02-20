from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    Point(10, 3),
    Point(13.9, 6.76),
    Point(12, 1.20),
]

v = Algorithm(BoundingBox(0, 25, 0, 25))
v.create_diagram(points=points, visualize_steps=False, verbose=True)

for point in v.points:
    print(point.cell_size(2), end=",")