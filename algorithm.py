from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt

from nodes.events import SiteEvent, CircleEvent
from nodes.internal_node import Breakpoint, InternalNode
from nodes.leaf_node import Arc, LeafNode
from nodes.smart_node import SmartNode
from nodes.smart_tree import SmartTree


class Algorithm:
    def __init__(self):

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

    def initialize(self, points):

        # Store the points for visualization
        self.points = points

        # Initialize event queue with all site events.
        for index, point in enumerate(points):
            # Give each point a letter, so we can look at letters rather than coordinates when debugging
            point.name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index % 26]

            # Create site event
            site_event = SiteEvent(point=point)
            self.event_queue.put(site_event)

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

        # TODO: finish all half edges using a bounding box
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

        # 5. TODO: Create half edge records
        pass

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

        if left_event is not None:
            self.event_queue.put(left_event)

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)

        self.beach_line.visualize()
        self.beach_line = SmartTree.balance_and_propagate(root)
        self.beach_line.visualize()

    def handle_circle_event(self, event: CircleEvent):

        # 1. Delete the leaf γ that represents the disappearing arc α from T.
        arc_node: LeafNode = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor
        self.update_breakpoints(event, self.beach_line, self.sweep_line, arc_node, predecessor, successor)

        # Delete all circle events involving arc from the event queue.
        if predecessor is not None and predecessor.get_value().circle_event is not None:
            predecessor.get_value().circle_event.remove()
        if successor is not None and successor.get_value().circle_event is not None:
            predecessor.get_value().circle_event.remove()

        # 2. TODO: Create half-edge records

        # 3. Check if breakpoints converge for the triples with former left and former right as middle arcs
        former_left = predecessor
        former_right = successor

        node_a, node_b, node_c = former_left.predecessor, former_left, former_left.successor
        node_c, node_d, node_e = former_right.predecessor, former_right, former_right.successor

        left_event = CircleEvent.create_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line)
        right_event = CircleEvent.create_circle_event(node_c, node_d, node_e, sweep_line=self.sweep_line)

        if left_event is not None:
            self.event_queue.put(left_event)

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)

    @staticmethod
    def update_breakpoints(event, root, sweep_line, arc_node, predecessor, successor):
        left_breakpoint = Breakpoint(breakpoint=(predecessor.get_value().origin, arc_node.get_value().origin))
        right_breakpoint = Breakpoint(breakpoint=(arc_node.get_value().origin, successor.get_value().origin))

        # If the arc node is a left child, then its parent is the node with right_breakpoint
        if arc_node.is_left_child():

            # Replace the right breakpoint by the right node
            root = arc_node.parent.replace_leaf(arc_node.parent.right, root)
            # SmartTree.propagating_balance(arc_node.parent.right)

            # Find the left breakpoint
            breakpoint: InternalNode = SmartTree.find(root, key=left_breakpoint.get_intersection(sweep_line).x,
                                        sweep_line=sweep_line)

            # Update the breakpoint
            if breakpoint is not None:
                breakpoint.data.breakpoint = (breakpoint.get_value().breakpoint[0], successor.get_value().origin)

        # If the arc node is a right child, then its parent is the breakpoint on the left
        else:

            # Replace the right breakpoint by the right node
            root = arc_node.parent.replace_leaf(arc_node.parent.left, root)
            # SmartTree.propagating_balance(arc_node.parent.left)

            # Find the left breakpoint
            breakpoint = SmartTree.find(root, key=right_breakpoint.get_intersection(sweep_line).x,
                                        sweep_line=sweep_line)

            # Update the breakpoint
            if breakpoint is not None:
                breakpoint.data.breakpoint = (predecessor.get_value().origin, breakpoint.get_value().breakpoint[1])

        return root

    def visualize(self, y, current_event):

        # Create 1000 equally spaced points between -10 and 10 and setup plot window
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

        for event in self.event_queue.queue:
            if isinstance(event, CircleEvent):
                plot_circle(event)

        # Plot points
        for point in self.points:
            x, y = point.x, point.y
            ax.scatter(x=[x], y=[y], s=50, color="black")

        plt.show()