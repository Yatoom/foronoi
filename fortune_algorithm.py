from queue import PriorityQueue

import math

from data_structures.bin_search_tree import AVLTree, Node
from data_structures.dcel import *


class InternalNode:
    """
    An internal node of the beach line.
    The internal nodes represent the breakpoints on the beach line.
    """

    def __init__(self):
        """
        The breakpoint is stored by an ordered tuple of sites (p_i, p_j) where p_i defines the parabola left of the
        breakpoint and p_j defines the parabola to the right. Furthermore, the internal node v has a pointer to the half
        edge in the doubly connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the
        half-edges of the edge being traced out by the breakpoint represented by v.
        """
        self.breakpoint: tuple = (None, None)
        self.pointer = None

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

            # Use quadratic formula to solve the problem
            z0 = 2 * (i.y - l)
            z1 = 2 * (i.y - l)

            a = 1 / z0 - 1 / z1
            b = -2 * (i.x / z0 - j.x / z1)
            c = (i.x ** 2 + i.y ** 2 - l ** 2) / z0 - (j.x ** 2 + j.y ** 2 - l ** 2) / z1

            result.x = (-b - math.sqrt(b ** 2 - 4 * a * c) / (2 * a))

        # Calculate the y-coordinate from the x coordinate
        result.y = (p.y ** 2 + (p.x - result.x) ** 2 - l ** 2) / (2 * p.y - 2 * l)

        return result


class Leaf:
    """

    """


class Point:
    """
    A simple point
    """
    x = None
    y = None


class CirclePoint(Point):
    """
    A point that represents the lowest point of a circle.
    It has a pointer to the leaf in the beach line that represents the arc that will disappear in the event.
    """
    pointer = None


class BreakPoint:
    """
    The breakpoint of the arcs are (where they intersect).
    Breakpoints are stored in the internal nodes of the beach line. Every internal node has a pointer to a half-edge
    in the doubly-connected edge list of the Voronoi diagram. More precisely, v has a pointer to one of the half-edges
    of the edge being traced out by the breakpoint represented by v.
    """
    points: tuple = (None, None)


class Arc:
    """
    Each leaf of beach line, representing an arc α, stores one pointer to a node in the event queue, namely, the node
    that represents the circle event in which α will disappear. This pointer is None if no circle event exists where α
    will disappear, or this circle event has not been detected yet.
    """
    pointer = None


class Voronoi:
    def __init__(self):

        # Event queue
        # -----------
        # - Event queue is implemented as a priority queue.
        # - The priority of an event is its y-coordinate.
        # - Stores the upcoming events that are already known.
        # - For a site event, we simply store the site itself.
        # - For a circle event, the event point that we store is the lowest point of the circle,
        #   with a pointer to the leaf in the beach line that represents the arc that will disappear
        #   in the event.
        # - All events will be stored as (priority_number, data)
        self.event_queue = PriorityQueue()

        # Status structure
        # ----------------
        # - The status structure, or beach line is represented by a balanced binary search tree
        # - Leaves correspond to the arcs of the beach line
        # - Leftmost leaf represents the leftmost arc, the next leaf represents the second leftmost arc, etc.
        # - Each leaf stores the site that defines the arc it represents
        # - Internal nodes represent the breakpoints on the beach line
        # - A breakpoint is stored at an internal node by an ordered tuple of sites (p_i, p_j),
        #   where p_i defines the parabola left of the breakpoint and p_j the one on the right
        # - We store pointers to the other two data structures used during the sweep
        #   - Each leaf stores one pointer to a node in the event queue, namely the node that
        #     represents the circle event in which the arc will disappear.
        #   - This pointer is None if no circle event exists, or the circle hasn't been detected yet
        #   - Finally, every internal node has a pointer to a half-edge in the doubly connected edge list
        #     of the Voronoi diagram. (v has a pointer to one of the half edges of the edge being traced out
        #     by the breakpoint represented by v)
        self.beach_line = AVLTree()

        # Doubly connected edge list
        self.doubly_connected_edge_list = []

    def create_diagram(self, points: list):
        # Initialize event queue with all site events.
        for point in points:
            priority = point.y
            self.event_queue.put((priority, point))

        while not self.event_queue.empty():
            priority, event = self.event_queue.get()

            if isinstance(event, CirclePoint):
                leaf = event.pointer
                self.handle_circle_event(leaf)
            elif isinstance(event, Point):
                self.handle_site_event(event)
            else:
                raise Exception("Not a Point or CirclePoint.")

    def handle_site_event(self, point):
        # 1. If the beach line tree is empty, we insert point
        if self.beach_line.root is None:
            self.beach_line.insert(point.x, point)
            return

        # 2.1 Search the beach line tree for the arc above the point
        # In other words, we shoot a ray up from the point that we found at the sweep line. So, we need to see where
        # the breakpoints of the arcs are (where they intersect). The breakpoints are stored in the internal nodes of
        # the beach line, while the arcs are stored within the leaves


        # # 2.1 Search the beach line tree for the arc above point
        # assert (self.beach_line.root is not None)
        # arc = self.beach_line.find(point.x)
        #
        # # 2.2 If the leaf representing the arc has a pointer to a circle event in the event_queue, we have a false
        # #     alarm, and the it must be deleted from the event_queue
        # if isinstance(arc, CirclePoint) and arc.leaf is not None and arc.leaf in self.event_queue.queue:
        #     self.event_queue.queue.remove(arc.pointer)
        #
        # # 3. Replace the leaf that represents the arc with a subtree having three leaves.
        # #    - The middle leaf stores the new site
        # #    - The other two leaves store the site p_j that was originally stored with the arc
        # #    - Store the tuples (p_j, p_i) and (p_i, p_j) representing the new breakpoints at the two internal nodes.
        # point_i = point
        # point_j = arc.pointer
        # middle_leaf = Node(point_i.x, point_i)
        # left_leaf = Node(point_j.x, point_j)
        # right_leaf = Node(point_j.x, point_j)
        # first_internal_node = Node(point_i.x, (point_i, point_j))
        # second_internal_node = Node(point_j.x, (point_j, point_j.x))

    def handle_circle_event(self, circle_point):
        raise NotImplementedError()

        # 7. The internal nodes still present in the beach line correspond to the half-infinite edges
        # of the Voronoi diagram.
        # Compute a bounding box that contains all vertices of the Voronoi diagram in its interior,
        # and attach the half-infinite edges to the bounding box by updating the doubly-connected
        # edge list appropriately

        # 8. Traverse the half-edges of the doubly connected edge list to cell records and the
        # pointers to and from them.
