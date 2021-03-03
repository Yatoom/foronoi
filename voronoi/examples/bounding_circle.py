from voronoi import Voronoi
from voronoi.graph.bounding_circle import BoundingCircle

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
    vis_steps=True,            # Visualize intermediate steps
    vis_result=True,           # Visualize the final result
    vis_tree=True,             # Print the binary tree at each step
    vis_before_clipping=True,  # Visualize the intermediate final result before clipping
    verbose=True               # Print the event queue and events that handled at each step
)

edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points
