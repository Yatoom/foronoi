from voronoi import Voronoi, Polygon, Visualizer

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

# Create the Voronoi diagram
v.create_diagram(points=points)

# Visualize the Voronoi diagram
Visualizer(v) \
    .plot_sites(show_labels=True) \
    .plot_edges(show_labels=False) \
    .plot_vertices() \
    .show()

# Some examples of how to access properties from the Voronoi diagram:
edges = v.edges                    # A list of all edges
vertices = v.vertices              # A list of all vertices
sites = v.sites                    # A list of all cell points (a.k.a. sites)
v.sites[0].cell_size()             # Calculate cell size for a cell point
v.sites[0].get_coordinates()       # Get the coordinates of the borders around a cell point
v.sites[0].get_borders()           # Get the borders around the cell point
v.sites[0].get_vertices()          # Get the vertices of the borders
v.vertices[0].connected_edges()    # Get all the edges that are connected to this vertex
position = v.vertices[0].position  # Get the position of this vertex
origin = v.edges[0].origin         # Get the vertex that the edge originates in
target = v.edges[0].target         # Get the vertex that the edge points to
