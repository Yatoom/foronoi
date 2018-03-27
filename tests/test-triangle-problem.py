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
    Point(45, 13),
    # Point(43, 85),
    Point(57, 71),
    Point(39, 82),
    # Point(49, 22),
    Point(61, 81),
    # Point(22, 95),
    # Point(17, 78),
    # Point(23, 77),
    # Point(27, 90),
]

v = Algorithm(polygon)
v.create_diagram(points=points, visualize_steps=False, verbose=False)

calculated = [p.cell_size(2) for p in v.points]
print(calculated)