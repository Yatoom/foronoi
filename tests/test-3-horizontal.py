from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(2, 2.5),
    Point(4, 2.5),
    Point(6, 2.5),
]

v = Algorithm(BoundingBox(0, 8, 0, 10))
v.create_diagram(points=points, visualize_steps=False, verbose=True)

for point in v.points:
    print(point.cell_size(2), end=",")