import random
from voronoi import Voronoi, Polygon, Point, VoronoiObserver

# Width and height of the triangle
width = 100
height = 100

# Number of points to generate
n_points = 10

# Print the randomly generated input points
print_input = True

# Create the triangle
triangle = Polygon([
    (0, height),
    (width, height),
    (width / 2, 0)
])

# Print the input points
points = [
    Point(76, 98),
    Point(13, 75),
    Point(43, 36),
    Point(38, 34),
    Point(61, 35),
    Point(46, 14),
    Point(66, 91),
    Point(68, 40),
    Point(86, 81),
    Point(53, 42),
]

# Initialize the algorithm
v = Voronoi(triangle)

# Attach observer that visualizes Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(
        visualize_steps=True,
        visualize_before_clipping=True,
        visualize_result=True,

        # Settings to put into the visualizer
        settings=dict(polygon=True, edges=True, vertices=True, sites=True,
                      outgoing_edges=False, beach_line=True, arcs=True, border_to_site=False, scale=1,
                      edge_labels=False, site_labels=False, triangles=False),

        # Callback that saves the figure every step
        callback=lambda observer, figure: figure.savefig(f"output/{observer.n_messages:2d}.png")
    )

)

# Start the procedure
v.create_diagram(
    points=[(p.x, p.y) for p in points],
)
