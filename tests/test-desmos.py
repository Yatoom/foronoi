from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.point import Point

points = [
    # Points from https://www.desmos.com/calculator/ejatebvup4
    Point(4.6, 11.44),
    Point(10, 15.44),
    Point(10, 3),
    Point(12.7, 10.6),
    Point(8.7, 7.7),
    Point(13.9, 6.76),
    Point(7.1, 4.24),

    # Point(2.3, 12),
    # Point(12, 1.20),
    # Point(5.3, 2),
    # Point(3.4, 2.9),
    # Point(7.8, 8.4),
    # Point(10.1, 3.46),
    # Point(11.2, 7.54),

]

v = Algorithm(BoundingBox(0, 25, 0, 25))
v.create_diagram(points=points, visualize_steps=False, verbose=False)

print(v.vertices)

for vertex in v.vertices:
    for edge in vertex.incident_edges:
        start = edge.get_origin()
        end = edge.twin.get_origin()

        # If the origin is not known yet, then they are infinite half-edges.
        # The bounding box should then be applied to finish them and give them an origin on the bounding box.

        if start is not None:
            print(start.x, start.y)

        if end is not None:
            print(end.x, end.y)