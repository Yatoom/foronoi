import math
from decimal import *

from foronoi.events.event import Event
from foronoi.graph.coordinate import Coordinate
from foronoi.nodes.leaf_node import LeafNode
from foronoi.nodes.arc import Arc


class CircleEvent(Event):
    circle_event = True

    def __init__(self, center: Coordinate, radius: Decimal, arc_node: LeafNode, point_triple=None, arc_triple=None):
        """
        A circle event.

        Parameters
        ----------
        center: Coordinate
            The center coordinate of the circle (where the new vertex will appear)
        radius: Decimal
            The radius of the circle
        arc_node: LeafNode
            Pointer to the node in the beach line tree that holds the arc that will disappear
        point_triple: (Point, Point, Point)
            The triple of points that caused the event
        arc_triple: (Arc, Arc, Arc)
            The triple of arcs related to the points
        """
        self.center = center
        self.radius = radius
        self.arc_pointer = arc_node
        self.is_valid = True
        self.point_triple = point_triple
        self.arc_triple = arc_triple

    def __repr__(self):
        return f"CircleEvent({self.point_triple}, y-radius={self.center.yd - self.radius:.2f}, y={self.center.yd:.2f}, radius={self.radius:.2f})"

    @property
    def xd(self):
        """
        The x-coordinate (in Decimal format) of the center of the circle, which functions as the secondary priority of this event.

        Returns
        -------
        x: Decimal
        """
        return self.center.xd

    @property
    def yd(self):
        """
        The y-coordinate (in Decimal format) of the bottom of the circle, which functions as the primary priority of this event.

        Returns
        -------
        y: Decimal
        """
        return self.center.yd - self.radius

    def _get_triangle(self):
        return (
            (self.point_triple[0].xd, self.point_triple[0].yd),
            (self.point_triple[1].xd, self.point_triple[1].yd),
            (self.point_triple[2].xd, self.point_triple[2].yd),
        )

    def remove(self):
        """
        Mark this circle event as a false alarm.

        Returns
        -------
        self: CircleEvent
        """
        self.is_valid = False
        return self

    @staticmethod
    def create_circle_event(left_node: LeafNode, middle_node: LeafNode, right_node: LeafNode, sweep_line) -> "CircleEvent":
        """
        Checks if the breakpoints converge, and inserts circle event if required.

        Parameters
        ----------
        left_node: LeafNode
            The node that represents the arc on the left
        middle_node: LeafNode
            The node that represents the arc in the middle
        right_node: LeafNode
            The node that represents the arc on the right
        sweep_line: Decimal
            The y-coordinate of the sweep line

        Returns
        -------
        circleEvent: CircleEvent or None
            The circle event or None if no circle event needs to be inserted
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
            return CircleEvent(center=Coordinate(x, y), radius=radius, arc_node=middle_node, point_triple=(a, b, c),
                               arc_triple=(left_arc, middle_arc, right_arc))

        return None

    @staticmethod
    def create_circle(a, b, c):
        """
        Create a circle from three coordinates.

        Parameters
        ----------
        a: Coordinate
        b: Coordinate
        c: Coordinate

        Returns
        -------
        x: Decimal
            The x-coordinate of the center of the circle
        y: Decimal
            The y-coordinate of the center of the circle
        radius: Decimal
            The radius of the circle
        """

        # Algorithm from O'Rourke 2ed p. 189
        A = b.xd - a.xd
        B = b.yd - a.yd
        C = c.xd - a.xd
        D = c.yd - a.yd
        E = (b.xd - a.xd) * (a.xd + b.xd) + (b.yd - a.yd) * (a.yd + b.yd)
        F = (c.xd - a.xd) * (a.xd + c.xd) + (c.yd - a.yd) * (a.yd + c.yd)
        G = 2 * ((b.xd - a.xd) * (c.yd - b.yd) - (b.yd - a.yd) * (c.xd - b.xd))

        if G == 0:
            # Points are all on one line (collinear), so no circle can be made
            return False

        # Center and radius of the circle
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G

        radius = Decimal.sqrt((a.xd - x) ** 2 + (a.yd - y) ** 2)

        return x, y, radius
