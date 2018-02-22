from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    Point(8.333, 8.333),
    Point(8.333, 26),
    Point(16.667, 8.333),
    Point(26, 17.667)
]

v = Algorithm(BoundingBox(0, 30, 0, 30))
v.create_diagram(points=points, visualize_steps=True, verbose=True)

for point in v.points:
    print(point.cell_size(2), end=",")