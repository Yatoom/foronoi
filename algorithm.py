from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
import copy
import numpy as np
from sklearn.preprocessing import normalize

from nodes.diagram import HalfEdge, Vertex, BoundingBox
from nodes.events import SiteEvent, CircleEvent, Event
from nodes.internal_node import Breakpoint, InternalNode
from nodes.leaf_node import Arc, LeafNode
from nodes.smart_node import SmartNode
from nodes.smart_tree import SmartTree
from nodes.point import Point
import matplotlib.patches as patches


class Algorithm:
    def __init__(self, bounding_box=None):

        # The bounding box around the edge
        self.bounding_box = bounding_box

        # Event queue for upcoming site and circle events
        self.event_queue = PriorityQueue()

        # Root of beach line
        self.beach_line: SmartNode = None

        # Doubly connected edge list
        self.doubly_connected_edge_list = []

        # Position of the sweep line, initialized at the max
        self.sweep_line = float("inf")

        # Store arcs for visualization
        self.arc_list = []

        # Store points for visualization
        self.points = None

        # Half edges for visualization
        self.edges = []

        # List of vertices
        self.vertices = []

    def initialize(self, points):

        # Store the points for visualization
        self.points = points

        # Initialize event queue with all site events.
        for index, point in enumerate(points):
            # # Give each point a letter, so we can look at letters rather than coordinates when debugging
            # point.name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index % 26]

            # Create site event
            site_event = SiteEvent(point=point)
            self.event_queue.put(site_event)

        for index, event in enumerate(self.event_queue.queue):
            event.point.name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index % 26]

        return self.event_queue

    def create_diagram(self, points: list, visualize=True):

        # Initialize all points
        self.initialize(points)

        while not self.event_queue.empty():
            print("Queue", self.event_queue.queue)

            # Pop the event queue with the highest priority
            event = self.event_queue.get()

            # Handle circle events
            if isinstance(event, CircleEvent) and event.is_valid:

                # Update sweep line position
                self.sweep_line = event.y

                # Debugging
                print(f"-> Handle circle event at {event.y} with center {event.center}")

                # Handle the event
                self.handle_circle_event(event)

                # Visualization
                if visualize:
                    print(self.beach_line.visualize())
                    self.visualize(self.sweep_line, current_event=event)

            # Handle site events
            elif isinstance(event, SiteEvent):

                # Update sweep line position
                self.sweep_line = event.y

                # Debugging
                print(f"-> Handle site event at {event.y} with point {event.point}")

                # Handle the event
                self.handle_site_event(event)

                # Visualization
                if visualize:
                    self.beach_line.visualize()
                    self.visualize(self.sweep_line, current_event=event)

        # Final visualization
        self.beach_line.visualize()
        self.visualize(-1000, current_event="Result")

        # Clip all the infinite edges by a bounding box
        self.finish_edges(self.edges, self.bounding_box)

        # TODO: Create half edges for the bounding box

        # Final visualization
        self.beach_line.visualize()
        self.visualize(-1000, current_event="Final result")
        return None

    def handle_site_event(self, event: SiteEvent):

        # Create a new arc
        new_point = event.point
        new_arc = Arc(origin=new_point)
        self.arc_list.append(new_arc)

        # 1. If the beach line tree is empty, we insert point
        if self.beach_line is None:
            self.beach_line = LeafNode(new_arc)
            return

        # 2. Search the beach line tree for the arc above the point
        arc_node_above_point = SmartTree.find_leaf_node(self.beach_line, key=new_point.x, sweep_line=self.sweep_line)
        arc_above_point = arc_node_above_point.get_value()

        print("Arc above point:", arc_above_point)

        # 3. Remove potential false alarm
        if arc_above_point.circle_event is not None:
            arc_above_point.circle_event.remove()

        # 4. Replace leaf with new sub tree that represents the two new intersections on the arc above the point
        #
        #            (p_j, p_i)
        #              /     \
        #             /       \
        #           p_j    (p_i, p_j)
        #                   /     \
        #                  /       \
        #                p_i       p_j
        point_i = new_point
        point_j = arc_above_point.origin
        breakpoint_left = Breakpoint(breakpoint=(point_j, point_i))
        breakpoint_right = Breakpoint(breakpoint=(point_i, point_j))

        root = InternalNode(breakpoint_left)
        root.left = LeafNode(Arc(origin=point_j, circle_event=None))
        root.right = InternalNode(breakpoint_right)
        root.right.left = LeafNode(new_arc)
        root.right.right = LeafNode(Arc(origin=point_j, circle_event=None))

        self.beach_line = arc_node_above_point.replace_leaf(replacement=root, root=self.beach_line)

        # 5. Create half edge records
        A, B = point_j, point_i
        AB = breakpoint_left
        BA = breakpoint_right

        # Edge AB -> BA with incident point B
        AB.edge = HalfEdge(B, origin=AB)

        # Edge BA -> AB with incident point A
        BA.edge = HalfEdge(A, origin=BA, twin=breakpoint_left.edge)

        # Append one of the edges to the list (we can get the other by using twin)
        self.edges.append(AB.edge)

        # 6. Check if breakpoints are going to converge with the arcs to the left and to the right
        #
        #            (p_j, p_i)
        #  \           /     \
        #   \         /       \
        # node_a ... node_b   (p_i, p_j)
        #                   /     \              /
        #                  /       \            /
        #              node_c    node_d ... node_e
        #
        node_a, node_b, node_c = root.left.predecessor, root.left, root.right.left
        node_c, node_d, node_e = root.right.left, root.right.right, root.right.right.successor

        left_event = CircleEvent.create_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line)
        right_event = CircleEvent.create_circle_event(node_c, node_d, node_e, sweep_line=self.sweep_line)

        # Check if the circles are on the correct side
        if left_event is not None and left_event.x > node_c.data.origin.x:
            left_event = None

        if right_event is not None and right_event.x < node_c.data.origin.x:
            right_event = None

        if left_event is not None:
            self.event_queue.put(left_event)
            node_b.data.circle_event = left_event

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)
            node_d.data.circle_event = right_event

        # 7. Rebalance the tree
        self.beach_line = SmartTree.balance_and_propagate(root)

    def handle_circle_event(self, event: CircleEvent):

        # 1. Delete the leaf γ that represents the disappearing arc α from T.
        arc_node: LeafNode = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor
        updated, removed = self.update_breakpoints(self.beach_line, self.sweep_line, arc_node, predecessor, successor)

        # Delete all circle events involving arc from the event queue.
        if predecessor is not None and predecessor.get_value().circle_event is not None:
            predecessor.get_value().circle_event.remove()
        if successor is not None and successor.get_value().circle_event is not None:
            successor.get_value().circle_event.remove()

        # 2. Create half-edge records

        # Get the location where the breakpoints converge
        convergence_point = event.center

        # Create a vertex
        v = Vertex(point=convergence_point)
        self.vertices.append(v)

        # Connect the two old edges to the vertex
        updated.edge.origin = v
        removed.edge.origin = v
        v.incident_edges.append(updated.edge)
        v.incident_edges.append(removed.edge)

        # Get the incident points
        C = updated.breakpoint[0]
        B = updated.breakpoint[1]

        # Create a new edge for the new breakpoint, where the edge originates in the new breakpoint
        updated.edge = HalfEdge(B, origin=updated, twin=HalfEdge(C, origin=v))
        v.incident_edges.append(updated.edge.twin)

        # Add to list for visualization
        self.edges.append(updated.edge)

        # 3. Check if breakpoints converge for the triples with former left and former right as middle arcs
        former_left = predecessor
        former_right = successor

        node_a, node_b, node_c = former_left.predecessor, former_left, former_left.successor
        node_c, node_d, node_e = former_right.predecessor, former_right, former_right.successor

        left_event = CircleEvent.create_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line)
        right_event = CircleEvent.create_circle_event(node_c, node_d, node_e, sweep_line=self.sweep_line)

        # Check if the circles are on the correct side
        if left_event is not None and left_event.x > node_c.data.origin.x:
            left_event = None

        if right_event is not None and right_event.x < node_c.data.origin.x:
            right_event = None

        if left_event is not None:
            self.event_queue.put(left_event)
            node_b.data.circle_event = left_event

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)
            node_d.data.circle_event = right_event

    @staticmethod
    def update_breakpoints(root, sweep_line, arc_node, predecessor, successor):

        # If the arc node is a left child, then its parent is the node with right_breakpoint
        if arc_node.is_left_child():

            # Replace the right breakpoint by the right node
            root = arc_node.parent.replace_leaf(arc_node.parent.right, root)

            # Mark the right breakpoint as removed
            removed = arc_node.parent.data

            # Rebalance the tree
            root = SmartTree.balance_and_propagate(root)

            # Find the left breakpoint
            left_breakpoint = Breakpoint(breakpoint=(predecessor.get_value().origin, arc_node.get_value().origin))
            query = InternalNode(left_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint: InternalNode = SmartTree.find_value(root, query, compare, sweep_line=sweep_line)

            # Update the breakpoint
            if breakpoint is not None:
                breakpoint.data.breakpoint = (breakpoint.get_value().breakpoint[0], successor.get_value().origin)

            # Mark this breakpoint as updated
            updated = breakpoint.data if breakpoint is not None else None

        # If the arc node is a right child, then its parent is the breakpoint on the left
        else:

            # Replace the left breakpoint by the left node
            root = arc_node.parent.replace_leaf(arc_node.parent.left, root)

            # Mark the left breakpoint as removed
            removed = arc_node.parent.data

            # Rebalance the tree
            root = SmartTree.balance_and_propagate(root)

            # Find the right breakpoint
            right_breakpoint = Breakpoint(breakpoint=(arc_node.get_value().origin, successor.get_value().origin))
            query = InternalNode(right_breakpoint)
            compare = lambda x, y: hasattr(x, "breakpoint") and x.breakpoint == y.breakpoint
            breakpoint: InternalNode = SmartTree.find_value(root, query, compare, sweep_line=sweep_line)

            # Update the breakpoint
            if breakpoint is not None:
                breakpoint.data.breakpoint = (predecessor.get_value().origin, breakpoint.get_value().breakpoint[1])

            # Mark this breakpoint as updated
            updated = breakpoint.data if breakpoint is not None else None

        return updated, removed

    def visualize(self, y, current_event):

        # Create 1000 equally spaced points between -10 and 10 and setup plot window
        x = np.linspace(-25, 25, 100)
        fig, ax = plt.subplots(figsize=(7, 7))
        plt.title(current_event)
        plt.ylim((self.bounding_box.bottom - 5, self.bounding_box.top + 5))
        plt.xlim((self.bounding_box.left - 5, self.bounding_box.right + 5))

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

        # Plot half-edges
        for edge in self.edges:
            if not edge.removed:
                start = edge.get_origin(y)
                end = edge.twin.get_origin(y)
                plt.plot([start.x, end.x], [start.y, end.y], color="blue")

        if isinstance(current_event, CircleEvent):
            plot_circle(current_event)

        for event in self.event_queue.queue:
            if isinstance(event, CircleEvent):
                plot_circle(event)

        # Draw bounding box
        ax.add_patch(
            patches.Rectangle(
                (self.bounding_box.left, self.bounding_box.bottom),  # (x,y)
                self.bounding_box.right - self.bounding_box.left,  # width
                self.bounding_box.top - self.bounding_box.bottom,  # height
                fill=False
            )
        )

        # Plot points
        for point in self.points:
            x, y = point.x, point.y
            ax.scatter(x=[x], y=[y], s=50, color="black")

        plt.show()

    def finish_edges(self, edges, bounding_box):
        for edge in edges:
            if edge.get_origin() is None:
                x, y = self.finish_edge(edge, bounding_box)
                v = Vertex(point=Point(x, y))
                v.incident_edges.append(edge)
                edge.origin = v

            if edge.twin.get_origin() is None:
                x, y = self.finish_edge(edge.twin, bounding_box)
                v = Vertex(point=Point(x, y))
                v.incident_edges.append(edge.twin)
                edge.twin.origin = v

        return edges

    @staticmethod
    def finish_edge(edge, bounding_box):

        # Start should be a breakpoint
        start = edge.get_origin(y=bounding_box.bottom)

        # End should be a vertex
        end = edge.twin.get_origin(y=bounding_box.bottom)

        # Check distances
        speed_y = start.y - end.y
        speed_x = start.x - end.x

        # Check directions
        right = speed_x > 0
        up = speed_y > 0

        # Get walls to check
        x = bounding_box.right if right else bounding_box.left
        y = bounding_box.top if up else bounding_box.bottom

        # Get distance to wall
        dist_x = x - end.x
        dist_y = y - end.y

        # Check whether x or y wall is being hit first
        time_x = dist_x / speed_x
        time_y = dist_y / speed_y

        if time_x < time_y:
            slope = (start.y - end.y) / (start.x - end.x)
            return x, slope * (x - start.x) + start.y

        slope = (start.x - end.x) / (start.y - end.y)
        return slope * (y - start.y) + start.x, y