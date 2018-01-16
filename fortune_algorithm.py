from queue import PriorityQueue

import math
from typing import Union

from data_structures.bin_search_tree import AVLTree, Node
from data_structures.dcel import *
from data_structures.types import Point, CirclePoint, Breakpoint, Arc


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

        # Position of the sweep line, initialized at the max
        self.sweep_line = float("inf")

    def create_diagram(self, points: list):
        # Sort points on y-value (high to low)
        # points = sorted(points, key=lambda p: p.y, reverse=True)

        # Initialize event queue with all site events.
        for point in points:

            self.event_queue.put((point.priority(), point))

        print("Initial priority queue:", self.event_queue.queue)

        while not self.event_queue.empty():
            _, event = self.event_queue.get()
            print("Event:", event)
            print("Priority queue:", self.event_queue.queue)

            if isinstance(event, CirclePoint):
                self.sweep_line = event.y
                leaf = event.pointer
                self.handle_circle_event(leaf)
            elif isinstance(event, Point):
                self.sweep_line = event.y
                self.handle_site_event(event)
            else:
                raise Exception("Not a Point or CirclePoint.")

                # 7. The internal nodes still present in the beach line correspond to the half-infinite edges
                # of the Voronoi diagram.
                # Compute a bounding box that contains all vertices of the Voronoi diagram in its interior,
                # and attach the half-infinite edges to the bounding box by updating the doubly-connected
                # edge list appropriately

                # 8. Traverse the half-edges of the doubly connected edge list to cell records and the
                # pointers to and from them.

    def handle_site_event(self, point):
        # 1. If the beach line tree is empty, we insert point
        if self.beach_line.root is None:
            arc = Arc(origin=point, pointer=None)
            self.beach_line.insert(arc, state=self.sweep_line)
            print("Beach line:", self.beach_line)
            return

        # 2.1 Search the beach line tree for the arc above the point
        # In other words, we shoot a ray up from the point that we found at the sweep line. So, we need to see where
        # the breakpoints of the arcs are (where they intersect). The breakpoints are stored in the internal nodes of
        # the beach line, while the arcs are stored within the leaves
        arc_node = self.beach_line.find_arc_node(x=point.x, y=self.sweep_line)
        arc = arc_node.value
        # arc = self.beach_line.find_arc_above_point(point=point, sweep_line=self.sweep_line)

        # 2.2 If the leaf representing the arc has a pointer to a circle event in the event_queue, we have a false
        #     alarm, and the it must be deleted from the event_queue
        if arc.pointer is not None and isinstance(arc.pointer, CirclePoint) and arc.pointer in self.event_queue:
            self.event_queue.queue.remove(arc.pointer)

        # 3. Replace the leaf that represents the arc with a subtree having three leaves.
        #    - The middle leaf stores the new site
        #    - The other two leaves store the site p_j that was originally stored with the arc
        #    - Store the tuples (p_j, p_i) and (p_i, p_j) representing the new breakpoints at the two internal nodes.

        point_i = point
        point_j = arc.origin
        breakpoint_j_i = Breakpoint(breakpoint=(point_j, point_i))
        breakpoint_i_j = Breakpoint(breakpoint=(point_i, point_j))

        # Create a tree with two breakpoints and three arcs.
        #
        #            (p_j, p_i)
        #              /     \
        #             /       \
        #           p_j    (p_i, p_j)
        #                   /     \
        #                  /       \
        #                p_i       p_j
        root = Node(breakpoint_j_i)
        root.left = Node(point_j)
        root.right = Node(breakpoint_i_j)
        root.right.left = point_i
        root.right.right = point_j

        # Replace this in the tree
        if arc_node == self.beach_line.root:
            self.beach_line.root = arc_node
        elif arc_node == arc_node.parent.left:
            arc_node.parent.left = root
        else:
            arc_node.parent.right = root

        # self.beach_line.replace_leaf(key=arc.x, replacement_tree=root)
        # self.beach_line.balance()

        # 4. Create new half-edge records in the Voronoi diagram structure for the
        #    edge separating V(p i ) and V(p j ), which will be traced out by the two new
        #    breakpoints.
        #    Note: The origins are breakpoints, but those breakpoints are still moving, so we don't know
        #    where exactly the start or end of a Voronoi edge is.
        half_edge_i, half_edge_j = self.create_half_edges(point_i, point_j)
        self.doubly_connected_edge_list.append(half_edge_i)
        self.doubly_connected_edge_list.append(half_edge_j)

        # TODO: Something with origin

        # 5. Check the triple of consecutive arcs where the new arc for p i is the left arc
        #    to see if the breakpoints converge. If so, insert the circle event into Q and
        #    add pointers between the node in T and the node in Q. Do the same for the
        #    triple where the new arc is the right arc.
        pass

        # TODO: Implement this

    @staticmethod
    def create_half_edges(point_i, point_j):

        # Create half edges
        half_edge_i = HalfEdge()
        half_edge_j = HalfEdge()

        # Set inner points
        half_edge_i.inner_point = point_i
        half_edge_j.inner_point = point_j

        # Set twins
        half_edge_j.twin = half_edge_i
        half_edge_i.twin = half_edge_j

        return half_edge_i, half_edge_j

    def handle_circle_event(self, circle_point):
        # TODO: Implement this
        raise NotImplementedError()
