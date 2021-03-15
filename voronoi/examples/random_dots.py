import numpy as np
from voronoi import Voronoi, Polygon

# Generate 200 random
from voronoi import Polygon

points = np.random.rand(100, 2)
points = np.concatenate([points, points])
polygon = Polygon([
    (0, 0),
    (1, 0),
    (1, 1),
    (0, 1)
])

print(points)

# Initialize the algorithm
v = Voronoi(polygon)

# Create the diagram
v.create_diagram(
    points=points
)