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
bounding_circle = BoundingCircle(5., 5., 15.)

v = Voronoi(bounding_circle)

v.create_diagram(points=points, vis_before_clipping=True, vis_steps=False, verbose=False, vis_result=True, vis_tree=True)

edges = v.edges
vertices = v.vertices
arcs = v.arcs
points = v.points
