from algorithm import Algorithm
from nodes.point import Point

# Testing square grid
bounding_box = (100, 100)
points = []
for i in range(25, 0, -5):
    for j in range(0, 25, 5):
        points.append(Point(j, i))
v = Algorithm()
v.create_diagram(points=points, visualize=True)