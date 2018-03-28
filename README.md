# Voronoi
![](https://raw.githubusercontent.com/Yatoom/voronoi/master/triangle.gif?token=AEAsSe31OClBjmuokyt2nDPS4AxIglUVks5axApWwA%3D%3D)'

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
```
Calculate the shell size for each point:
```python
for point in v.points:
    print(point.cell_size())
```
Output:
```
11.529761904761905
15.064062500000006
11.75
10.520833333333329
7.640625
5.946354166666666
9.423363095238095
```

Get coordinates for a point:
```python
v.points[0].get_coordinates()
```
Output:
```python
[
    Point(0.167, 5.333), 
    Point(4.5, 1.0), 
    Point(4.643, 0.0), 
    Point(2.5, 0), 
    Point(0, 2.5), 
    Point(0, 5)
]
```

## Testing
To run unit tests, run the following comand.
```
python3 -m "nose" voronoi/tests/unit.py
```