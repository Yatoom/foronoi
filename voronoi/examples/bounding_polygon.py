from voronoi import Voronoi, Polygon, Visualizer, TreeVisualizer, VoronoiObserver, TreeObserver

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

# # Attach a Voronoi Observer that monitors and visualizes the construction of
# # the Voronoi Diagram step-by-step
# v.attach_observer(VoronoiObserver(visualize_steps=True))
#
# # If you want to see what happens in the binary tree, you could use the TreeObserver
# v.attach_observer(TreeObserver(visualize_steps=True))

# Create the Voronoi diagram
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

# Visualize the tree
TreeVisualizer() \
    .plot(v.beach_line) \
    .render("output/tree.dot", view=True)
