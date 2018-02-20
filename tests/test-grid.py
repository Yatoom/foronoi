from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

# Testing square grid
points = []
for i in range(25, 0, -5):
    for j in range(0, 25, 5):
        points.append(Point(j, i))
v = Algorithm(BoundingBox(-5, 30, -5, 30))
v.create_diagram(points=points, visualize_steps=False)