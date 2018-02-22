# Voronoi
An implementation of Fortune's algorithm as described in "Computational Geometry: Algorithms and Applications" by de Berg et al. in python.

## Example usage
```python
from algorithm import Algorithm
from graph import Point, BoundingBox

# Define a set of points
points = [
    Point(4.6, 11.44),
    Point(12.7, 10.6),
    Point(13.9, 6.76),
    Point(8.7, 7.7),
    Point(7.1, 4.24),
]

# Define a bounding box
bounding_box = BoundingBox(0, 25, 0, 25)

# Initalize the algorithm
v = Algorithm(bounding_box)

# Create the diagram
v.create_diagram(points=points, visualize_steps=True, verbose=True, visualize_result=True)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Calculate the sell size for each  point
for point in v.points:
    print(point.cell_size())
```