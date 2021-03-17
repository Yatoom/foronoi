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

# Generate the points
points = []
while len(points) < n_points:
    p = Point(random.randint(0, width), random.randint(0, height))

    # Check if the point is inside the triangle
    if triangle.inside(p):
        points.append(p)

# Print the input points
if print_input:
    print("points = [")
    for point in points:
        print(f"    Point({point.x}, {point.y}),")
    print("]")

# Initialize the algorithm
v = Voronoi(triangle)

# Attach observer that visualizes Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(
        visualize_steps=True,

        # Callback that saves the figure every step
        callback=lambda observer, figure: figure.savefig(f"output/{observer.n_messages}.png"))
)

# Start the procedure
v.create_diagram(
    points=[(p.x, p.y) for p in points],
)