from fortune_algorithm import Voronoi, Point, Breakpoint

# Testing breakpoint
j = Point(4.6, 11.44)  # This one comes first
i = Point(12.7, 10.6)  # This one comes second

bp_j_i = Breakpoint(breakpoint=(j, i))
bp_i_j = Breakpoint(breakpoint=(i, j))

print(bp_j_i.get_intersection(8))
print(bp_i_j.get_intersection(8))
print(bp_i_j.get_key(8))
print("")

# Testing create diagram
bounding_box = (100, 100)
points = [
    # Points from https://www.desmos.com/calculator/ejatebvup4
    Point(4.6, 11.44),
    Point(12.7, 10.6),
    Point(8.7, 7.7),
    Point(13.9, 6.76),
    Point(7.1, 4.24),
]

v = Voronoi()
v.create_diagram(points=points)
