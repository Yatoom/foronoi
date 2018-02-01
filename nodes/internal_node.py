import math
from nodes.smart_node import SmartNode
from data_structures.types import Point


class InternalNode(SmartNode):
    def __init__(self, data: Breakpoint):
        super().__init__(data)

    def get_key(self, sweep_line=None):
        return self.data.get_intersection(sweep_line).x

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data[0].name}{self.data[1].name}"


class Breakpoint:
    """
    A breakpoint between two arcs.
    """

    def __init__(self, breakpoint: tuple):
        """
        The breakpoint is stored by an ordered tuple of sites (p_i, p_j) where p_i defines the parabola left of the
        breakpoint and p_j defines the parabola to the right. Furthermore, the internal node v has a pointer to the half
        edge in the doubly connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the
        half-edges of the edge being traced out by the breakpoint represented by v.
        :param breakpoint: A tuple of two points that caused two arcs to intersect
        """
        self.breakpoint = breakpoint

    def get_intersection(self, l):
        """
        Calculate the coordinates of the intersection
        Modified from https://www.cs.hmc.edu/~mbrubeck/voronoi.html

        :param l: (float) The position (y-coordinate) of the sweep line
        :return: (float) The coordinates of the breakpoint
        """

        # Get the points
        i, j = self.data.breakpoint

        # Initialize the resulting point
        result = Point()
        p: Point = i

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