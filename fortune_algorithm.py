from queue import PriorityQueue
from data_structures.bin_search_tree import AVLTree
from data_structures.dcel import *


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
    leaf = None


class Voronoi:
    def create_diagram(self, points: list):

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
        event_queue = PriorityQueue()

        # Initialize event queue with all site events.
        for point in points:
            priority = point.y
            event_queue.put((priority, point))

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
        #     represents the circle event in which alpha will disappear.
        #   - This pointer is None if no circle event exists, or the circle hasn't been detected yet
        #   - Finally, every internal node has a pointer to a half-edge in the doubly connected edge list
        #     of the Voronoi diagram. (v has a pointer to one of the half edges of the edge being traced out
        #     by the breakpoint represented by v)
        beach_line = AVLTree()

        # Doubly connected edge list
        doubly_connected_edge_list = []

        while not event_queue.empty():
            priority, event = event_queue.get()

            if isinstance(event, CirclePoint):
                leaf = event.leaf
                self.handle_circle_event(leaf)
            elif isinstance(event, Point):
                self.handle_site_event(event)
            else:
                raise Exception("Not a Point or CirclePoint.")

    def handle_site_event(self, point):
        raise NotImplementedError()

    def handle_circle_event(self, circle_point):
        raise NotImplementedError()
