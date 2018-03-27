from algorithm import Algorithm
from graph import Point, Polygon

x = 100
y = 100
n = 10

polygon_points = [
    Point(0, y),
    Point(x, y),
    Point(x/2, 0)
]

polygon = Polygon(polygon_points)

points = [
    Point(54, 90),
    Point(69, 85),
    Point(41, 26),
    Point(69, 46),
    Point(54, 13),
    Point(54, 26),
    Point(5, 95), # <--
    Point(16, 85), # <--
    Point(45, 53),
    Point(22, 59),
]

v = Algorithm(polygon)
v.create_diagram(points=points, visualize_steps=False, verbose=False)

calculated = [p.cell_size(2) for p in v.points]
print(calculated)