from fortune_algorithm import Voronoi, Point

bounding_box = (100, 100)
points = [
    # Points from https://www.desmos.com/calculator/ejatebvup4
    Point(4.6, 11.44),
    Point(12.7, 10.6),
    Point(8.7, 7.7),
    Point(7.1, 4.24),
]

v = Voronoi()
v.create_diagram(points=points)
