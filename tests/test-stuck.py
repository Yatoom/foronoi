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
points = [
    Point(57, 75),
    Point(35, 85),
    Point(92, 98),
    Point(81, 87),
]

v = Algorithm(polygon)
v.create_diagram(points=points, visualize_steps=False, verbose=True)

for point in v.points:
    print(point.cell_size(2), end=",")