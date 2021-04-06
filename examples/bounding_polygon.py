import os
import matplotlib.pyplot as plt

from foronoi import Voronoi, Polygon, Visualizer, TreeVisualizer, VoronoiObserver, TreeObserver

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

# Optional: attach observer that visualizes Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(

        # Settings to put into the visualizer
        settings=dict(polygon=True, edges=True, vertices=True, sites=True,
                      outgoing_edges=False, border_to_site=False, scale=1,
                      edge_labels=False, site_labels=False, triangles=False, arcs=False),

        # Callback that saves the figure every step
        callback=lambda observer, figure: figure.savefig(f"output/voronoi/{observer.n_messages:02d}.png")
    )
)

# Optional: attach observer that visualizes the tree every step
v.attach_observer(
    TreeObserver(
        # Callback that saves the figure every step
        callback=lambda observer, dot: dot.render(f"output/tree/{observer.n_messages:02d}")
    )
)

# Create the output directory if it doesn't exist
if not os.path.exists("output"):
    os.mkdir("output")

if not os.path.exists("output/tree/"):
    os.mkdir("output/tree/")

if not os.path.exists("output/voronoi/"):
    os.mkdir("output/voronoi/")

# Create the Voronoi diagram
v.create_diagram(points=points)

# Get properties
edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.sites

# Plotting
Visualizer(v, canvas_offset=1) \
    .plot_sites(points, show_labels=True) \
    .plot_edges(edges, show_labels=False) \
    .plot_vertices(vertices) \
    .plot_border_to_site() \
    .show()

# Visualize the tree
TreeVisualizer() \
    .plot(v.status_tree) \
    .render("output/tree.dot", view=True)
