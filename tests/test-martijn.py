from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(2.241, 3.594),
    Point(3.568, 3.968),
    Point(6.401, 16.214),
    Point(2.925, 18.298),
]

v = Algorithm(BoundingBox(-1, 26, -1, 26))
v.create_diagram(points=points, visualize_steps=True, verbose=True, visualize_result=True)
for point in v.points:
    print(point.cell_size(2), end=",")