# Voronoi
![](https://raw.githubusercontent.com/Yatoom/voronoi/master/triangle.gif?token=AEAsSZ1cdj9o218Avqx9vd1zuHvsb397ks5axNTqwA%3D%3D)

A Python implementation of Fortune's algorithm based on the description of "Computational Geometry: Algorithms and Applications" by de Berg et al. The algorithm handles the special cases described in the book. The bounding box is generalized to handle a convex polygon.

## Manual Installation

First, clone the repository and then install the package.
```bash
git clone https://github.com/Yatoom/voronoi.git
cd voronoi
python setup.py install
```
Note: you need to use `sudo python3 setup.py install` on most Linux distributions.

## Example usage

Example that uses a polygon as a bounding box.

```python
from voronoi import Voronoi, Polygon, Point, BoundingBox

# Define a set of points
points = [
    Point(2.5, 2.5),
    Point(4, 7.5),
    Point(7.5, 2.5),
    Point(6, 7.5),
    Point(4, 4),
    Point(3, 3),
    Point(6, 3),
]

# Define a bounding box
polygon = Polygon([
    Point(2.5, 10),
    Point(5, 10),
    Point(10, 5),
    Point(10, 2.5),
    Point(5, 0),
    Point(2.5, 0),
    Point(0, 2.5),
    Point(0, 5),
])

# Initialize the algorithm
v = Voronoi(polygon)

# Create the diagram
v.create_diagram(points=points, vis_steps=False, verbose=False, vis_result=True, vis_tree=True)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Calculate the sell size for each  point
for point in v.points:
    print(point.cell_size())
```
## Testing
To run unit tests, run the following comand.
```
python3 -m "nose" voronoi/tests/unit.py
```
