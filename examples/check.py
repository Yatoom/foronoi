from foronoi import Voronoi, Polygon, Visualizer, Point, VoronoiObserver
from foronoi.graph import HalfEdge, Vertex

# Define some points (a.k.a sites or cell points)
points = [
    (2.5, 2.5), (4, 7.5), (7.5, 2.5), (6, 7.5), (4, 4), (3, 3), (6, 3)
]

# Define a bounding box / polygon
polygon = Polygon([
    (2.5, 10), (5, 10), (10, 5), (10, 2.5), (5, 0), (2.5, 0), (0, 2.5), (0, 5)
])

# Initialize the algorithm
v = Voronoi(polygon)

# Optional: visualize the voronoi diagram at every step.
# You can find more information in the observers.py example file
# v.attach_observer(
#     VoronoiObserver()
# )

# Create the Voronoi diagram
v.create_diagram(points=points)

# Visualize the Voronoi diagram
Visualizer(v) \
    .plot_sites(show_labels=False) \
    .plot_edges(show_labels=False) \
    .plot_vertices() \
    .show()