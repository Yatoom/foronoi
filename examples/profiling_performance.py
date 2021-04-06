from foronoi import Voronoi, Polygon
import cProfile
import pstats


def profiler(command, filename="profile.stats", n_stats=20):
    """Profiler for a python program

    Runs cProfile and outputs ordered statistics that describe
    how often and for how long various parts of the program are executed.

    Parameters
    ----------
    command: str
        Command string to be executed.
    filename: str
        Name under which to store the stats.
    n_stats: int or None
        Number of top stats to show.
    """

    cProfile.run(command, filename)
    stats = pstats.Stats(filename).strip_dirs().sort_stats("cumtime")
    return stats.print_stats(n_stats or {})


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

# Profile the construction of the voronoi diagram
profiler('v.create_diagram(points=points)')
