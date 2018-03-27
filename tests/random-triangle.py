import random

from algorithm import Algorithm
from graph import Polygon, Point

x = 100
y = 100
n = 10
print_input = True

polygon_points = [
    Point(0, y),
    Point(x, y),
    Point(x/2, 0)
]

polygon = Polygon(polygon_points)

points = []
while len(points) < n:
    p = Point(random.randint(0, x), random.randint(0, y))
    if polygon.inside(p):
        points.append(p)

if print_input:
    print("points = [")
    for point in points:
        print(f"    Point({point.x}, {point.y}),")
    print("]")

v = Algorithm(polygon)
v.create_diagram(points=points, vis_steps=False, verbose=False, vis_tree=False)