from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(10, 10),
    Point(10, 20),
]

v = Algorithm(BoundingBox(0, 25, 0, 25))
v.create_diagram(points=points, visualize_steps=False, verbose=True)

print(points[0].cell_size())