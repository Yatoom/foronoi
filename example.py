# Polygon
from voronoi.algorithm import Algorithm

from voronoi import BoundingBox

polygon = BoundingBox(-10, 10, -10, 10)

# Points
points = [
    (0, 5),
    (5, 0),
    (-5, -5)
]

v = Algorithm(polygon)
v.create_diagram(points=points)