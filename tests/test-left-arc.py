from algorithm import Algorithm
from graph import Point, BoundingBox

points = [
    Point(3.125, 3.125),
    Point(9.375, 3.125),
    Point(15.625, 3.125),
    Point(21.875, 3.125),
    Point(3.125, 9.375),
]

v = Algorithm(BoundingBox(0, 25, 0, 25))
v.create_diagram(points=points, visualize_steps=False, verbose=False, visualize_result=True)

sizes = [39.06, 58.59, 117.19, 156.25, 253.91]
calculated = [p.cell_size(2) for p in v.points]
print(calculated)
points = v.points
assert (sizes == calculated)


print("Done")