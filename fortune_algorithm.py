from queue import PriorityQueue

import math
from typing import Union
import matplotlib.pyplot as plt
import numpy as np
from sympy.geometry import Triangle
from sympy.geometry import Point as P
import numpy as np
from data_structures.bin_search_tree import AVLTree, Node
from data_structures.dcel import *
from data_structures.types import Point, Breakpoint, Arc, CircleEvent, SiteEvent


class Voronoi:
    def __init__(self):

        self.arc_list = []

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

        # Store points for visualization
        self.points = None

    def create_diagram(self, points: list, visualize=True):
        # Initialize event queue with all site events.
        self.points = points
        for index, point in enumerate(points):
            point.name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index % 26]  # Easy for debugging
            site_event = SiteEvent(point=point)
            self.event_queue.put((site_event.priority, site_event))

        print("Initial priority queue:", self.event_queue.queue)

        while not self.event_queue.empty():

            _, event = self.event_queue.get()
            if isinstance(event, CircleEvent) and event.is_valid:
                self.sweep_line = event.y
                if visualize:
                    self.visualize(self.sweep_line, current_event=event)
                self.handle_circle_event(event)
            elif isinstance(event, SiteEvent):
                self.sweep_line = event.y
                self.handle_site_event(event)
                if visualize:
                    self.visualize(self.sweep_line, current_event=event)
            else:
                raise Exception("Not a Point or CirclePoint.")

            if visualize:
                self.beach_line.visualize()




            # 7. The internal nodes still present in the beach line correspond to the half-infinite edges
            # of the Voronoi diagram.
            # Compute a bounding box that contains all vertices of the Voronoi diagram in its interior,
            # and attach the half-infinite edges to the bounding box by updating the doubly-connected
            # edge list appropriately

            # 8. Traverse the half-edges of the doubly connected edge list to cell records and the
            # pointers to and from them.

    def handle_site_event(self, event: SiteEvent):
        print(f"Site event at {event.y} with point {event.point}")

        # Create a new arc
        new_point = event.point
        new_arc = Arc(origin=new_point)
        self.arc_list.append(new_arc)  # For visualization

        # 1. If the beach line tree is empty, we insert point
        if self.beach_line.root is None:
            self.beach_line.insert(new_arc, state=self.sweep_line)
            return

        # 2.1 Search the beach line tree for the arc above the point
        arc_node_above_point = self.beach_line.find_arc_node(x=new_point.x, y=self.sweep_line)
        arc_above_point: Arc = arc_node_above_point.value

        # 2.2 If the leaf representing the arc has a pointer to a circle event in the event_queue, we have a false
        #     alarm, and the it must be deleted from the event_queue
        if arc_above_point.circle_event is not None:
            arc_above_point.circle_event.remove()

        # 3. Replace the leaf that represents the arc with a subtree having three leaves.
        #    - The middle leaf stores the new site
        #    - The other two leaves store the site p_j that was originally stored with the arc
        #    - Store the tuples (p_j, p_i) and (p_i, p_j) representing the new breakpoints at the two internal nodes.

        point_i = new_point
        point_j = arc_above_point.origin
        breakpoint_left = Breakpoint(breakpoint=(point_j, point_i))
        breakpoint_right = Breakpoint(breakpoint=(point_i, point_j))
        breakpoint_left.left_arc = arc_above_point
        breakpoint_left.right_arc = new_arc
        breakpoint_right.left_arc = new_arc
        breakpoint_right.right_arc = arc_above_point

        # Create a tree with two breakpoints and three arcs.
        #
        #            (p_j, p_i)
        #              /     \
        #             /       \
        #           p_j    (p_i, p_j)
        #                   /     \
        #                  /       \
        #                p_i       p_j
        root = Node(breakpoint_left)
        root.left = Node(Arc(origin=point_j, circle_event=None))
        root.right = Node(breakpoint_right)
        root.right.left = Node(new_arc)
        root.right.right = Node(Arc(origin=point_j, circle_event=None))

        # Replace this in the tree
        arc_node_above_point.replace(root, self.beach_line)

        # 4. Create new half-edge records in the Voronoi diagram structure for the
        #    edge separating V(p i ) and V(p j ), which will be traced out by the two new
        #    breakpoints.
        #            /
        #           /| <-- right breakpoint moves to the right
        #          / | <-- somewhere in middle is the origin of the half edges
        # \       /  |
        #  \     /|  | <-- left breakpoint moves to the left
        #   \___/  \/
        #
        # intersection = breakpoint_left.get_intersection(self.sweep_line)
        # half_edge_right = HalfEdge(origin=intersection, )
        # half_edge_left = HalfEdge(origin=intersection, )
        #
        # half_edge_i, half_edge_j = self.create_half_edges(point_i, point_j, breakpoint_right, breakpoint_left)
        # self.doubly_connected_edge_list.append(half_edge_i)
        # self.doubly_connected_edge_list.append(half_edge_j)

        # 5. Check the triple of consecutive arcs where the new arc for p i is the left arc
        #    to see if the breakpoints converge. If so, insert the circle event into Q and
        #    add pointers between the node in T and the node in Q. Do the same for the
        #    triple where the new arc is the right arc.
        #
        #            (p_j, p_i)
        #  \           /     \
        #   \         /       \
        # arc_a ... arc_b   (p_i, p_j)
        #                   /     \              /
        #                  /       \            /
        #                arc_i      arc_c ... arc_d
        #
        arc_b = root.left
        arc_i = root.right.left
        arc_c = root.right.right
        arc_a = self.beach_line.get_left_arc_node(arc_b)
        arc_d = self.beach_line.get_right_arc_node(arc_c)

        # Check if it converges with the left
        self.insert_circle_event(arc_a, arc_b, arc_i)

        # Check if it converts with the right
        self.insert_circle_event(arc_i, arc_c, arc_d)

    @staticmethod
    def create_half_edges(point_i, point_j, breakpoint_i_j, breakpoint_j_i):

        # Create half edges
        half_edge_i = HalfEdge()
        half_edge_j = HalfEdge()

        # Set inner points
        half_edge_i.inner_point = point_i
        half_edge_j.inner_point = point_j

        # Set twins
        half_edge_j.twin = half_edge_i
        half_edge_i.twin = half_edge_j

        # The o is the origin of a half edge. The origins are the breakpoints of the arcs of i and j.
        # The half-edges point in clock-wise order.
        #                     o
        #             *j     //
        #                   //
        #                  //      *i
        #                  o
        # Remember that the left breakpoint is (j, i) and the right breakpoint is (i, j)
        # The origin for j will therefore be the breakpoint (i, j) and the origin for i is (j, i)
        # Once they have been traced out, the breakpoints should be replaced by fixed points.
        half_edge_i.origin = breakpoint_j_i
        half_edge_j.origin = breakpoint_i_j

        return half_edge_i, half_edge_j

    def handle_circle_event(self, event: CircleEvent):
        print(f"Handle circle event at {event.y} with center {event.center}")

        # Get the arc node
        arc_node: Node = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor

        # Say we have three arcs a, b and c. Arc a is in the middle, b on the right and c on the left. Arc a was found
        # first, b was the second and c the third. Arcs c and b are now going to move towards each other. That means
        # that the part between (c, a) and (a, b) is going to disappear: arc a, which is now stored as `arc_node`.
        # To get (c, a) we take the parent of the leaf. To get (a, b), we need to go up in the tree to find it.
        grandfather = arc_node.parent.parent
        ancestor = grandfather.parent

        # The arc that moves over the breakpoints from the left
        overlapping_arc = arc_node.parent.left
        grandfather.right = overlapping_arc

        # Update the (a, b) node to be (c, b)
        left, right = ancestor.value.breakpoint
        ancestor.value.breakpoint = (overlapping_arc.value.origin, right)

        # Delete all circle events involving arc from the event queue.
        if predecessor is not None and predecessor.value.circle_event is not None:
            predecessor.value.circle_event.remove()
        if successor is not None and successor.value.circle_event is not None:
            predecessor.value.circle_event.remove()

        # 2. Add the center of the circle causing the event as a vertex record to the
        #   doubly-connected edge list D storing the Voronoi diagram under construction.
        #   Create two half-edge records corresponding to the new breakpoint
        #   of the beach line. Set the pointers between them appropriately. Attach the
        #   three new records to the half-edge records that end at the vertex.

        # TODO
        vertex = Vertex(x=event.center.x, y=event.center.y)

        # 3. Check the new triple of consecutive arcs that has the former left neighbor
        #    of α as its middle arc to see if the two breakpoints of the triple converge.
        #    If so, insert the corresponding circle event into Q. and set pointers between
        #    the new circle event in Q and the corresponding leaf of T. Do the same for
        #    the triple where the former right neighbor is the middle arc.
        former_left = predecessor
        former_right = successor

        # Check if it converges with the left [find] [predecessor] [arc_node]
        if former_left is not None:
            middle_arc = former_left
            left_arc = former_left.predecessor
            right_arc = former_left.successor
            self.insert_circle_event(left_arc, middle_arc, right_arc)

        # Check if it converts with the right
        if former_right is not None:
            middle_arc = former_right
            left_arc = former_right.predecessor
            right_arc = former_right.successor
            self.insert_circle_event(left_arc, middle_arc, right_arc)

    def insert_circle_event(self, left_arc: Node, middle_arc: Node, right_arc: Node):
        """
        Checks if the breakpoints converge, and inserts circle event if required.
        :param left_arc: The node that represents the arc on the left
        :param middle_arc: The node that represents the arc on the middle
        :param right_arc: The node that represents the arc on the right
        :return: The circle event or None if no circle event needs to be inserted
        """
        if left_arc is None or right_arc is None or middle_arc is None:
            return None

        a, b, c = left_arc.value.origin, middle_arc.value.origin, right_arc.value.origin
        x, y, radius = self.create_circle(a, b, c)
        circle_event = CircleEvent(center=Point(x, y), radius=radius, arc_node=middle_arc, triple=(a, b, c))
        if circle_event.y < self.sweep_line:
            print(f"Sweep line reached {self.sweep_line}. Circle event inserted for {circle_event.y}.")
            print(f"\t Arcs: {left_arc.value.origin}, {middle_arc.value.origin}, {right_arc.value.origin}")
            self.event_queue.put((circle_event.priority, circle_event))

        return circle_event

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
            pass

        # Center and radius of the circle
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G
        radius = math.sqrt(math.pow(a.x - x, 2) + math.pow(a.y - y, 2))
        return x, y, radius

    def visualize(self, y, current_event):
        # Create 1000 equally spaced points between -10 and 10
        x = np.linspace(-25, 25, 100)
        fig, ax = plt.subplots(figsize=(7, 7))
        plt.title(current_event)
        plt.ylim((0, 25))
        plt.xlim((0, 25))

        # Plot the sweep line
        ax.plot(x, x + y - x, color='black')

        # Plot all arcs
        plot_lines = []
        for arc in self.arc_list:
            plot_line = arc.get_plot(x, y)
            if plot_line is None:
                ax.axvline(x=arc.origin.x)
            else:
                ax.plot(x, plot_line, linestyle="--", color='gray')
                plot_lines.append(plot_line)
        if len(plot_lines) > 0:
            ax.plot(x, np.min(plot_lines, axis=0), color="black")

        # Plot circle events
        def plot_circle(evt):
            x, y = evt.center.x, evt.center.y
            radius = evt.radius
            circle = plt.Circle((x, y), radius, fill=False, color="#1f77b4", linewidth=1.2)
            triangle = plt.Polygon(evt.get_triangle(), fill=False, color="#ff7f0e", linewidth=1.2)
            ax.add_artist(circle)
            ax.add_artist(triangle)

        if isinstance(current_event, CircleEvent):
            plot_circle(current_event)

        for priority, event in self.event_queue.queue:
            if isinstance(event, CircleEvent):
                plot_circle(event)

        # Plot points
        for point in self.points:
            x, y = point.x, point.y
            ax.scatter(x=[x], y=[y], s=50, color="black")

        plt.show()
