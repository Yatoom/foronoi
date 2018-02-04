import math

from nodes.leaf_node import Arc, LeafNode
from nodes.point import Point


class Event:
    @property
    def x(self):
        return 0

    @property
    def y(self):
        return 0

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x

        # Switch y axis
        return self.y > other.y

    def __eq__(self, other):
        if other is None:
            return None
        return self.y == other.y and self.x == other.x

    def __ne__(self, other):
        return not self.__eq__(other)


class SiteEvent(Event):
    def __init__(self, point: Point):
        """
        Site event
        :param point:
        """
        self.point = point

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y

    def __repr__(self):
        return f"SiteEvent(x={self.point.x}, y={self.point.y}, pl={self.point.player})"


class CircleEvent(Event):
    def __init__(self, center: Point, radius: float, arc_node: LeafNode, triple=None):
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
    def x(self):
        return self.center.x

    @property
    def y(self):
        return self.center.y - self.radius

    def get_triangle(self):
        return (
            (self.triple[0].x, self.triple[0].y),
            (self.triple[1].x, self.triple[1].y),
            (self.triple[2].x, self.triple[2].y),
        )

    def remove(self, verbose=False):
        if verbose:
            print(f"Circle event for {self.y} removed.")
        self.is_valid = False

    @staticmethod
    def create_circle_event(left_node: LeafNode, middle_node: LeafNode, right_node: LeafNode, sweep_line, verbose=False):
        """
        Checks if the breakpoints converge, and inserts circle event if required.
        :param sweep_line: Y-coordinate of the sweep line
        :param left_node: The node that represents the arc on the left
        :param middle_node: The node that represents the arc on the middle
        :param right_node: The node that represents the arc on the right
        :param verbose: Flag for printing debugging information
        :return: The circle event or None if no circle event needs to be inserted
        """

        # Check if any of the nodes is None
        if left_node is None or right_node is None or middle_node is None:
            return None

        # Get arcs from the nodes
        left_arc: Arc = left_node.get_value()
        middle_arc: Arc = middle_node.get_value()
        right_arc: Arc = right_node.get_value()

        # Get the points from the arcs
        a, b, c = left_arc.origin, middle_arc.origin, right_arc.origin

        # Check if we can create a circle event
        if CircleEvent.create_circle(a, b, c):

            # Create the circle
            x, y, radius = CircleEvent.create_circle(a, b, c)

            # Check if the bottom of the circle is below the sweep line
            if y - radius < sweep_line:

                # Debugging
                if verbose:
                    print(f"Sweep line reached {sweep_line}. Circle event inserted for {y - radius}.")
                    print(f"\t Arcs: {left_arc}, {middle_arc}, {right_arc}")

                # Create the circle event
                return CircleEvent(center=Point(x, y), radius=radius, arc_node=middle_node, triple=(a, b, c))

        return None

    @staticmethod
    def create_circle(a, b, c):
        # Algorithm from O'Rourke 2ed p. 189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0:
            # Points are all on one line (collinear), so no circle can be made
            return False

        # Center and radius of the circle
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G
        radius = math.sqrt(math.pow(a.x - x, 2) + math.pow(a.y - y, 2))

        return x, y, radius