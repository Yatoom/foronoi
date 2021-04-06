import os

from foronoi import Polygon, Voronoi, VoronoiObserver, TreeObserver, DebugObserver
from foronoi.visualization import Presets

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

# Attach a Voronoi observer that visualizes the Voronoi diagram every step
v.attach_observer(
    VoronoiObserver(

        # Settings to pass into the visualizer's plot_all() method.
        # - By default, the observer uses a set of minimalistic presets that are useful for visualizing during
        #   construction, clipping and the final result. Have a look at Presets.construction, Presets.clipping and
        #   Presets.final.
        # - These settings below will update the default presets used by the observer. For example, by default,
        #   the arc_labels are not shown, but below we can enable the arc labels. Other parameters can be found in
        #   the visualizer's plot_all() method.
        settings=dict(arc_labels=True, site_labels=True),

        # Callback that saves the figure every step
        # If no callback is provided, it will simply display the figure in a matplotlib window
        callback=lambda observer, figure: figure.savefig(f"output/voronoi/{observer.n_messages:02d}.png"),
        visualize_before_clipping=True
    )
)

# Attach observer that visualizes the tree every step. This is a binary tree data structure that keeps track of where
# the arcs and the breakpoints between the arcs are going.
v.attach_observer(
    TreeObserver(
        # Callback that saves the figure every step
        # If no callback is provided, it will render the figure in a window
        callback=lambda observer, dot: dot.render(f"output/tree/{observer.n_messages:02d}")
    )
)

# Attach a listener that listens to debug messages.
# If no callback is provided, it will print the messages.
v.attach_observer(DebugObserver(callback=lambda _: print(_)))

# Create the output directory if it doesn't exist
if not os.path.exists("output"):
    os.mkdir("output")

if not os.path.exists("output/tree/"):
    os.mkdir("output/tree/")

if not os.path.exists("output/voronoi/"):
    os.mkdir("output/voronoi/")

# Create the Voronoi diagram
v.create_diagram(points=points)
