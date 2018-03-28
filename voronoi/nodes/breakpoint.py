import math
from voronoi.graph.coordinate import Coordinate


class Breakpoint:
    """
    A breakpoint between two arcs.
    """

    def __init__(self, breakpoint: tuple, edge=None):
        """
        The breakpoint is stored by an ordered tuple of sites (p_i, p_j) where p_i defines the parabola left of the
        breakpoint and p_j defines the parabola to the right. Furthermore, the internal node v has a pointer to the half
        edge in the doubly connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the
        half-edges of the edge being traced out by the breakpoint represented by v.
        :param breakpoint: A tuple of two points that caused two arcs to intersect
        """

        # The tuple of the points whose arcs intersect
        self.breakpoint = breakpoint

        # The edge this breakpoint is tracing out
        self._edge = None
        self.edge = edge

    def __repr__(self):
        return f"Breakpoint({self.breakpoint[0].name}, {self.breakpoint[1].name})"

    def does_intersect(self):
        i, j = self.breakpoint
        return not (i.y == j.y and j.x < i.x)

    def get_intersection(self, l, max_y=None):
        """
        Calculate the coordinates of the intersection
        Modified from https://www.cs.hmc.edu/~mbrubeck/voronoi.html

        :param max_y: Bounding box top for clipping infinite breakpoints
        :param l: (float) The position (y-coordinate) of the sweep line
        :return: (float) The coordinates of the breakpoint
        """

        # Get the points
        i, j = self.breakpoint

        # Initialize the resulting point
        result = Coordinate()
        p: Coordinate = i

        # First we replace some stuff to make it easier
        a = i.x
        b = i.y
        c = j.x
        d = j.y
        u = 2 * (b - l)
        v = 2 * (d - l)

        # Handle the case where the two points have the same y-coordinate (breakpoint is in the middle)
        if i.y == j.y:
            result.x = (i.x + j.x) / 2

            if j.x < i.x:
                result.y = max_y or float('inf')
                return result

        # Handle cases where one point's y-coordinate is the same as the sweep line
        elif i.y == l:
            result.x = i.x
            p = j
        elif j.y == l:
            result.x = j.x
        else:
            # We now need to solve for x
            # 1/u * (x**2 - 2*a*x + a**2 + b**2 - l**2) = 1/v * (x**2 - 2*c*x + c**2 + d**2 - l**2)
            # Then we let Wolfram alpha do the heavy work for us, and we put it here in the code :D
            x = -(math.sqrt(
                v * (a ** 2 * u - 2 * a * c * u + b ** 2 * (u - v) + c ** 2 * u) + d ** 2 * u * (v - u) + l ** 2 * (
                    u - v) ** 2) + a * v - c * u) / (u - v)
            result.x = x

        # We have to re-evaluate this, since the point might have been changed
        a = p.x
        b = p.y
        x = result.x
        u = 2 * (b - l)

        # Handle degenerate case where parabolas don't intersect
        if u == 0:
            result.y = float("inf")
            return result

        # And we put everything back in y
        result.y = 1 / u * (x ** 2 - 2 * a * x + a ** 2 + b ** 2 - l ** 2)
        return result
