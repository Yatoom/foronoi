from algorithm import Algorithm
from graph import Point, BoundingBox

points = [
    Point(3.125, 3.125),
    Point(9.375, 3.125),
    Point(15.625, 3.125),
    Point(21.875, 3.125),
    Point(3.125, 9.375),
    Point(9.375, 9.375),
    Point(15.625, 9.375),
    Point(21.875, 9.375),
    Point(3.125, 15.625),
    Point(9.375, 15.625),
    Point(15.625, 15.625),
    Point(21.875, 15.625),
    Point(3.125, 21.875),
    Point(9.375, 21.875),
    Point(15.625, 21.875),
    Point(21.875, 21.875),
    Point(6.25, 18.75),
    Point(12.5, 18.75),
    Point(18.75, 18.75),
    Point(6.25, 12.5),
    Point(12.5, 12.5),
    Point(18.75, 12.5),
    Point(6.25, 6.25),
    Point(12.5, 6.25),
    Point(18.75, 6.25),
    Point(0.0, 12.5),
    Point(0.0, 18.75),
    Point(6.25, 25.0),
    Point(12.5, 25.0),
    Point(18.75, 25.0),
    Point(25.0, 18.75)
]

v = Algorithm(BoundingBox(-0.1, 25.1, -0.1, 25.1))
v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=True)

for point in v.points:
    print(point.cell_size(2), end=",")
