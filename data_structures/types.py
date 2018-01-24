import math
from abc import ABCMeta, abstractmethod


class Value(metaclass=ABCMeta):
    @abstractmethod
    def get_key(self, state):
        return NotImplemented

    @abstractmethod
    def get_label(self):
        return NotImplemented


class SimpleValue(Value):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_key(self, state):
        return self.key

    def get_label(self):
        return self.key

    def __repr__(self):
        return f"{self.key}: {self.value}"


class GameState:
    """
    The current state of the game.
    It will hold the settings of the game board and a list of place points
    """
    points = []

    def __init__(self, width: int = 100, height: int = 100, m: int = None, n: int = None):
        self.width = width
        self.height = height
        self.m = m
        self.n = n


class Point:
    """
    A simple point
    """

    def __init__(self, x=None, y=None, player: int = None, name=None):
        self.x: float = x
        self.y: float = y
        self.player = player
        self.name = name

    def __repr__(self):
        if self.name is not None:
            return f"Point_{self.name}"
        return f"Point({round(self.x, 3)}, {round(self.y, 3)})"

    # Methods below are solely so that the queue can sort these well
    def priority(self):
        return self.calc_priority(self.x, self.y)

    @staticmethod
    def calc_priority(x, y):
        y = round(y, 5) * 10**5
        x = round(x, 5) * 10**5
        yx = -int(y * 10**5 - x)
        return yx


class SiteEvent:
    def __init__(self, point: Point):
        """

        :param point:
        """
        self.point = point

    @property
    def y(self):
        return self.point.y

    @property
    def priority(self):
        return self.point.priority()

    def __repr__(self):
        return f"SiteEvent(x={self.point.x}, y={self.point.y}, pl={self.point.player})"


class CircleEvent:
    def __init__(self, center: Point, radius: float, arc_node: "Node", triple=None):
        """
        Circle event.

        :param y: Lowest point on the circle
        :param arc_node: Pointer to the node in the beach line tree that holds the arc that will disappear
        :param triple: The tuple of points that caused the event
        """
        self.center = center
        self.radius = radius
        self.arc_pointer = arc_node
        self.is_valid = True
        self.triple = triple

    def __repr__(self):
        return f"CircleEvent({self.center}, {round(self.radius, 3)})"

    @property
    def y(self):
        return self.center.y - self.radius

    @property
    def priority(self):
        return Point.calc_priority(self.center.x, self.y)

    def get_triangle(self):
        return (
            (self.triple[0].x, self.triple[0].y),
            (self.triple[1].x, self.triple[1].y),
            (self.triple[2].x, self.triple[2].y),
        )

    def remove(self):
        print(f"Circle event for {self.y} removed.")
        self.is_valid = False


class Breakpoint(Value):
    """
    A breakpoint between two arcs.
    The internal nodes represent the breakpoints on the beach line.
    """

    def __init__(self, breakpoint=(None, None), half_edge=None):
        """
        The breakpoint is stored by an ordered tuple of sites (p_i, p_j) where p_i defines the parabola left of the
        breakpoint and p_j defines the parabola to the right. Furthermore, the internal node v has a pointer to the half
        edge in the doubly connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the
        half-edges of the edge being traced out by the breakpoint represented by v.
        """
        self.breakpoint: tuple = breakpoint
        self.half_edge = half_edge

    def __repr__(self):
        return f"Breakpoint({self.breakpoint})"

    def get_label(self):
        return f"{self.breakpoint[0].name}{self.breakpoint[1].name}"

    def get_key(self, state=None):
        return self.get_intersection(state).x

    def get_intersection(self, l):
        """
        Calculate the coordinates of the intersection
        Modified from https://www.cs.hmc.edu/~mbrubeck/voronoi.html

        :param l: (float) The position (y-coordinate) of the sweep line
        :return: (float) The coordinates of the breakpoint
        """

        # Get the points
        i, j = self.breakpoint

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


class Arc(Value):
    """
    Each leaf of beach line, representing an arc α, stores one pointer to a node in the event queue, namely, the node
    that represents the circle event in which α will disappear. This pointer is None if no circle event exists where α
    will disappear, or this circle event has not been detected yet.
    """

    def __init__(self, origin: Point, circle_event: CircleEvent = None):
        """

        :param origin: The point that caused the arc
        :param circle_event: The pointer to the circle event in which the arc will disappear
        """
        self.origin: Point = origin
        self.circle_event: CircleEvent = circle_event

    def get_key(self, state=None):
        return self.origin.x

    def __repr__(self):
        return f"Arc(origin={self.origin}, circle_event={self.circle_event})"

    def get_label(self):
        return f"{self.origin.name}"

    def get_plot(self, x, l):
        l = l
        i = self.origin

        if i.y - l == 0:
            return None

        # Calculate the y value for each element of the x vector

        u = 2 * (i.y - l)
        v = (x**2 - 2*i.x * x + i.x**2 + i.y**2 - l**2)
        y = v/u

        return y
