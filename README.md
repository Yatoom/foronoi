# Foronoi
Fortune's algorithm for Voronoi diagrams. 

[![Build Status](https://travis-ci.org/Yatoom/voronoi.svg?branch=master)](https://travis-ci.org/Yatoom/voronoi)
[![Documentation Status](https://readthedocs.org/projects/voronoi/badge/?version=latest)](https://voronoi.readthedocs.io/en/latest/?badge=latest)


![](voronoi.gif)

Foronoi is a Python implementation of the Fortune’s algorithm based on the description of “Computational Geometry: Algorithms and Applications” by de Berg et al.

This algorithm is a sweep line algorithm that scans top down over the cell points and traces out the lines via breakpoints in between parabola’s (arcs). When lines converge, a circle event happens which inserts a new vertex.

[Documentation can be found here](https://voronoi.readthedocs.io/en/latest/).

## Pip Installation
```bash
pip install foronoi
```

## Manual Installation

First, clone the repository and then install the package.
```bash
git clone https://github.com/Yatoom/voronoi.git
cd foronoi
python setup.py install
```
Note: you need to use `sudo python3 setup.py install` on most Linux distributions.

## Example usage

Example that uses a polygon as a bounding box.

```python3
from foronoi import Voronoi, Polygon, Visualizer, VoronoiObserver

# Define some points (a.k.a sites or cell points)
points = [
    (2.5, 2.5),
    (4, 7.5),
    (7.5, 2.5),
    (6, 7.5),
    (4, 4),
    (3, 3),
    (6, 3),
]

# Define a bounding box / polygon
polygon = Polygon([
    (2.5, 10),
    (5, 10),
    (10, 5),
    (10, 2.5),
    (5, 0),
    (2.5, 0),
    (0, 2.5),
    (0, 5),
])

# Initialize the algorithm
v = Voronoi(polygon)

# Attach a Voronoi Observer that monitors and visualizes the construction of 
# the Voronoi Diagram step-by-step. See for more information 
# examples/quickstart.py or examples/observers.py.
v.attach_observer(VoronoiObserver())

# Create the diagram
v.create_diagram(points=points)

# Get properties. See more examples in examples/quickstart.py
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Plotting
# Note: plot_border_to_site() indicates with dashed line to which site a border 
# belongs. The site's first edge is colored green.
Visualizer(v, canvas_offset=1)\
    .plot_sites(show_labels=True)\
    .plot_edges(show_labels=False)\
    .plot_vertices()\
    .plot_border_to_site()\ 
    .show()

```
![image](https://user-images.githubusercontent.com/4205641/111237517-8a609800-85f5-11eb-8095-09001dd7b00e.png)



### Calculate the shell size for each point
```python
for point in v.sites:
    print(f"{point.xy} \t {point.area()}")
```
Output:
```
(2.5, 2.5) 	 11.529761904761905
(4, 7.5) 	 15.064062500000006
(7.5, 2.5) 	 11.75
(6, 7.5) 	 10.520833333333329
(4, 4) 	     7.640625
(3, 3) 	     5.946354166666666
(6, 3) 	     9.423363095238095
```

More examples can be found in the `voronoi/examples` folder.

### Get coordinates of the cell borders for a point
```python
vertices = v.sites[0].get_vertices()
coords = [(vertex.x, vertex.y) for vertex in vertices]
print(coords)
```
Output:
```python
[(0.167, 5.333), (4.5, 1.0), (4.643, 0.0), (2.5, 0), (0, 2.5), (0, 5)]
```

## Testing
To run unit tests, run the following comand.
```
python3 -m "nose" foronoi/tests/unit.py
```
