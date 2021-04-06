from foronoi import Voronoi, Visualizer
from foronoi.contrib import BoundingCircle

# Define a set of points
points = [
    (1, 2),
    (7, 13),
    (12, 6),
    (5, 5),
]

# Define a bounding circle
bounding_circle = BoundingCircle(5., 5., 9.)

v = Voronoi(bounding_circle)

v.create_diagram(
    points=points,
)

edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.sites

# Plotting
Visualizer(v, canvas_offset=1) \
    .plot_polygon()\
    .plot_sites(points, show_labels=True) \
    .plot_edges(edges, show_labels=False) \
    .plot_vertices(vertices) \
    .plot_border_to_site() \
    .show()
