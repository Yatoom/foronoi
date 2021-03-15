import math
from decimal import *

from voronoi.events.event import Event
from voronoi.graph.coordinate import DecimalCoordinate
from voronoi.nodes.leaf_node import LeafNode
from voronoi.nodes.arc import Arc


class CircleEvent(Event):
    circle_event = True

    def __init__(self, center: DecimalCoordinate, radius: Decimal, arc_node: LeafNode, point_triple=None, arc_triple=None):
        """
        Circle event.

        :param arc_node: Pointer to the node in the beach line tree that holds the arc that will disappear
        :param point_triple: The tuple of points that caused the event
        """
        self.center = center
        self.radius = radius
        self.arc_pointer = arc_node
        self.is_valid = True
        self.point_triple = point_triple
        self.arc_triple = arc_triple

    def __repr__(self):
        return f"CircleEvent({self.point_triple}, y-radius={self.center.y - self.radius:.2f}, y={self.center.y:.2f}, radius={self.radius:.2f})"

    @property
    def x(self):
        return self.center.x

    @property
    def y(self):
        return self.center.y - self.radius

    def get_triangle(self):
        return (
            (self.point_triple[0].x, self.point_triple[0].y),
            (self.point_triple[1].x, self.point_triple[1].y),
            (self.point_triple[2].x, self.point_triple[2].y),
        )

    def remove(self):
        self.is_valid = False
        return self

    @staticmethod
    def create_circle_event(left_node: LeafNode, middle_node: LeafNode, right_node: LeafNode, sweep_line) -> "CircleEvent":
        """
        Checks if the breakpoints converge, and inserts circle event if required.
        :param sweep_line: Y-coordinate of the sweep line
        :param left_node: The node that represents the arc on the left
        :param middle_node: The node that represents the arc on the middle
        :param right_node: The node that represents the arc on the right
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

            # Return circle event
            return CircleEvent(center=DecimalCoordinate(x, y), radius=radius, arc_node=middle_node, point_triple=(a, b, c),
                               arc_triple=(left_arc, middle_arc, right_arc))

        return None

    @staticmethod
    def create_circle(a, b, c):

        # Algorithm from O'Rourke 2ed p. 189
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = (b.x - a.x) * (a.x + b.x) + (b.y - a.y) * (a.y + b.y)
        F = (c.x - a.x) * (a.x + c.x) + (c.y - a.y) * (a.y + c.y)
        G = 2 * ((b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x))

        if G == 0:
            # Points are all on one line (collinear), so no circle can be made
            return False

        # Center and radius of the circle
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G

        radius = Decimal.sqrt((a.x - x) ** 2 + (a.y - y) ** 2)

        return x, y, radius
