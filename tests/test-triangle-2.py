from algorithm import Algorithm
from graph import Polygon, Point

x = 100
y = 100
n = 10

polygon_points = [
    Point(0, y),
    Point(x, y),
    Point(x / 2, 0)
]

polygon = Polygon(polygon_points)
points = [Point(x-13, 93), Point(x-20, 89), Point(x-33, 69)]

v = Algorithm(polygon)
v.create_diagram(points=points, visualize_steps=False, verbose=False)

for point in v.points:
    print(point.cell_size(2), end=",")