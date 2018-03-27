# Voronoi
![](https://raw.githubusercontent.com/Yatoom/voronoi/master/triangle.gif?token=AEAsSe31OClBjmuokyt2nDPS4AxIglUVks5axApWwA%3D%3D)'

A Python implementation of Fortune's algorithm based on the description of "Computational Geometry: Algorithms and Applications" by de Berg et al. The algorithm handles the special cases described in the book. The bounding box is generalized to handle a convex polygon.

## Example usage

Example that uses a polygon as a bounding box.

```python
from algorithm import Algorithm
from graph import Polygon, Point

# Define a set of points
voronoi_points = [
    Point(2.5, 2.5),
    Point(4, 7.5),
    Point(7.5, 2.5),
    Point(6, 7.5),
    Point(4, 4),
    Point(3, 3),
    Point(6, 3),
]

# Define a bounding box
polygon_points = [
    Point(2.5, 10),
    Point(5, 10),
    Point(10, 5),
    Point(10, 2.5),
    Point(5, 0),
    Point(2.5, 0),
    Point(0, 2.5),
    Point(0, 5),
]

# Initalize the algorithm
v = Algorithm(Polygon(polygon_points))

# Create the diagram
v.create_diagram(points=voronoi_points, vis_steps=False, verbose=False, vis_result=True, vis_tree=True)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Calculate the sell size for each  point
for point in v.points:
    print(point.cell_size())
```
