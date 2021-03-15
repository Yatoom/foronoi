from voronoi import Voronoi, Polygon, Visualizer
import matplotlib.pyplot as plt

# Define a set of points
from voronoi.observers.voronoi_observer import VoronoiObserver

points = [
    (2.5, 2.5),
    (4, 7.5),
    (7.5, 2.5),
    (6, 7.5),
    (4, 4),
    (3, 3),
    (6, 3),
]

# Define a bounding box
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

v.attach_observer(VoronoiObserver(visualize_steps=True))

# Create the diagram
v.create_diagram(points=points)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points

# Plotting
Visualizer(polygon, canvas_offset=1)\
    .plot_sites(points, show_labels=True)\
    .plot_edges(edges, show_labels=False)\
    .plot_vertices(vertices)\
    .show()
