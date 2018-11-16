from queue import PriorityQueue

from voronoi.graph import Point
from voronoi.graph import HalfEdge, Vertex, Algebra
from voronoi.nodes import LeafNode, Arc, Breakpoint, InternalNode
from voronoi.events import CircleEvent, SiteEvent
from voronoi.tree import SmartTree, SmartNode
from voronoi.visualization import visualize
from voronoi.visualization import Tell


class Algorithm:
    def __init__(self, bounding_poly=None):

        # The bounding box around the edge
        self.bounding_poly = bounding_poly

        # Event queue for upcoming site and circle events
        self.event_queue = PriorityQueue()

        # Root of beach line
        self.beach_line: SmartNode = None

        # Doubly connected edge list
        self.doubly_connected_edge_list = []

        # Position of the sweep line, initialized at the max
        self.sweep_line = float("inf")

        # Store arcs for visualization
        self.arcs = []

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
            # Create site event
            site_event = SiteEvent(point=point)
            self.event_queue.put(site_event)

        return self.event_queue

    def create_diagram(self, points: list, vis_steps=False, vis_result=False, vis_tree=False,
                       vis_before_clipping=False, verbose=False):
        """
        Create the Voronoi diagram.

        :param points: (list) The list of cell points to make the diagram for
        :param vis_steps: (bool) Visualize intermediate steps
        :param vis_result: (bool) Visualize the final result
        :param vis_tree: (bool) Visualize the status of the binary tree (text-based)
        :param vis_before_clipping: Visualize the intermediate final result before clipping
        :param verbose: (bool) Print debug information
        """

        points = [Point(x, y) for x, y in points]

        # Initialize all points
        self.initialize(points)
        index = 0

        # The first point (needed for bounding box)
        genesis_point = None

        while not self.event_queue.empty():

            Tell.print(verbose, "Queue", self.event_queue.queue)

            # Pop the event queue with the highest priority
            event = self.event_queue.get()

            # Set genesis point
            genesis_point = genesis_point or event.point

            # Handle circle events
            if isinstance(event, CircleEvent) and event.is_valid:
                # Update sweep line position
                self.sweep_line = event.y

                # Debugging
                Tell.print(
                    verbose,
                    f"-> Handle circle event at {event.y} with center {event.center} and arcs {event.point_triple}"
                )

                # Handle the event
                self.handle_circle_event(event, verbose=verbose)

                # Visualization
                if vis_steps and vis_tree:
                    self.beach_line.visualize()

                if vis_steps:
                    visualize(self.sweep_line, current_event=event, bounding_poly=self.bounding_poly,
                              points=self.points, vertices=self.vertices, edges=self.edges, arc_list=self.arcs,
                              event_queue=self.event_queue)

            # Handle site events
            elif isinstance(event, SiteEvent):

                # Give the points a simple name
                event.point.name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index % 26]
                index += 1

                # Update sweep line position
                self.sweep_line = event.y

                # Debugging
                Tell.print(verbose, f"-> Handle site event at {event.y} with point {event.point}")

                # Handle the event
                self.handle_site_event(event, verbose=verbose)

                # Visualization
                if vis_steps and vis_tree:
                    self.beach_line.visualize()

                if vis_steps:
                    visualize(y=self.sweep_line, current_event=event, bounding_poly=self.bounding_poly,
                              points=self.points, vertices=self.vertices, edges=self.edges, arc_list=self.arcs,
                              event_queue=self.event_queue)

        if vis_before_clipping:
            visualize(y=-1000, current_event="nothing", bounding_poly=self.bounding_poly,
                      points=self.points, vertices=self.vertices, edges=self.edges, arc_list=self.arcs,
                      event_queue=self.event_queue)

        # Finish with the bounding box
        self.edges, polygon_vertices = self.bounding_poly.finish_edges(self.edges, verbose)
        self.edges, self.vertices = self.bounding_poly.finish_polygon(self.edges, self.vertices, self.points)

        # Final visualization
        if vis_result:
            visualize(-1000, current_event="Final result", bounding_poly=self.bounding_poly,
                      points=self.points, vertices=self.vertices, edges=self.edges, arc_list=self.arcs,
                      event_queue=self.event_queue, calc_cell_sizes=True)

    def handle_site_event(self, event: SiteEvent, verbose=False):

        # Create a new arc
        new_point = event.point
        new_arc = Arc(origin=new_point)
        self.arcs.append(new_arc)

        # 1. If the beach line tree is empty, we insert point
        if self.beach_line is None:
            self.beach_line = LeafNode(new_arc)
            return

        # 2. Search the beach line tree for the arc above the point
        arc_node_above_point = SmartTree.find_leaf_node(self.beach_line, key=new_point.x, sweep_line=self.sweep_line)
        arc_above_point = arc_node_above_point.get_value()

        # 3. Remove potential false alarm
        if arc_above_point.circle_event is not None:
            arc_above_point.circle_event.remove(verbose=verbose)

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

        # Only insert right breakpoint into the tree if it actually intersects
        if breakpoint_right.does_intersect():
            root.right = InternalNode(breakpoint_right)
            root.right.left = LeafNode(new_arc)
            root.right.right = LeafNode(Arc(origin=point_j, circle_event=None))
        else:
            root.right = LeafNode(new_arc)

        self.beach_line = arc_node_above_point.replace_leaf(replacement=root, root=self.beach_line)

        # 5. Create half edge records
        A, B = point_j, point_i
        AB = breakpoint_left
        BA = breakpoint_right

        # Edge AB -> BA with incident point B
        AB.edge = HalfEdge(B, origin=AB)

        # Edge BA -> AB with incident point A
        BA.edge = HalfEdge(A, origin=BA, twin=AB.edge)

        # Append one of the edges to the list (we can get the other by using twin)
        self.edges.append(AB.edge)

        # Add first edges
        B.first_edge = B.first_edge or AB.edge
        A.first_edge = A.first_edge or BA.edge

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

        # If the right breakpoint does not intersect, we don't need to insert circle events.
        if not breakpoint_right.does_intersect():
            return

        node_a, node_b, node_c = root.left.predecessor, root.left, root.right.left
        node_c, node_d, node_e = node_c, root.right.right, root.right.right.successor

        self.check_circles((node_a, node_b, node_c), (node_c, node_d, node_e), verbose)

        # 7. Rebalance the tree
        self.beach_line = SmartTree.balance_and_propagate(root)

    def handle_circle_event(self, event: CircleEvent, verbose=False):

        # 1. Delete the leaf γ that represents the disappearing arc α from T.
        arc_node: LeafNode = event.arc_pointer
        predecessor = arc_node.predecessor
        successor = arc_node.successor

        # Update breakpoints
        self.beach_line, updated, removed, left, right = self.update_breakpoints(
            self.beach_line, self.sweep_line, arc_node, predecessor, successor)

        # Delete all circle events involving arc from the event queue.
        def remove(neighbor_event):
            if neighbor_event is None:
                return None
            return neighbor_event.remove()

        remove(predecessor.get_value().circle_event)
        remove(successor.get_value().circle_event)

        # 2. Create half-edge records

        # Get the location where the breakpoints converge
        convergence_point = event.center

        # Create a new edge for the new breakpoint, where the edge originates in the new breakpoint
        # Note: we only create the new edge if the vertex is still inside the bounding box
        # if self.bounding_poly.inside(event.center):
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

        new_edge = HalfEdge(B, origin=updated, twin=HalfEdge(C, origin=v))
        v.incident_edges.append(updated.edge.twin)

        # Add to list for visualization
        self.edges.append(new_edge)

        # Set previous and next
        left.edge.twin.set_next(new_edge.twin)  # yellow
        right.edge.twin.set_next(left.edge)  # orange
        new_edge.set_next(right.edge)  # blue

        # Let the updated breakpoint now point to the new edge
        updated.edge = new_edge

        # 3. Check if breakpoints converge for the triples with former left and former right as middle arcs
        former_left = predecessor
        former_right = successor

        node_a, node_b, node_c = former_left.predecessor, former_left, former_left.successor
        node_d, node_e, node_f = former_right.predecessor, former_right, former_right.successor

        self.check_circles((node_a, node_b, node_c), (node_d, node_e, node_f), verbose)

    def check_circles(self, triple_left, triple_right, verbose=False):
        node_a, node_b, node_c = triple_left
        node_d, node_e, node_f = triple_right

        left_event = CircleEvent.create_circle_event(node_a, node_b, node_c, sweep_line=self.sweep_line,
                                                     verbose=verbose)
        right_event = CircleEvent.create_circle_event(node_d, node_e, node_f, sweep_line=self.sweep_line,
                                                      verbose=verbose)

        # Check if the circles converge
        if left_event:
            if not Algebra.check_clockwise(node_a.data.origin, node_b.data.origin, node_c.data.origin,
                                           left_event.center):
                Tell.print(verbose, f"Circle {left_event.point_triple} not clockwise.")
                left_event = None

        if right_event:
            if not Algebra.check_clockwise(node_d.data.origin, node_e.data.origin, node_f.data.origin,
                                           right_event.center):
                Tell.print(verbose, f"Circle {right_event.point_triple} not clockwise.")
                right_event = None

        if left_event is not None:
            self.event_queue.put(left_event)
            node_b.data.circle_event = left_event

        if right_event is not None and left_event != right_event:
            self.event_queue.put(right_event)
            node_e.data.circle_event = right_event

        if left_event is not None:
            Tell.print(verbose, f"Left circle event created for {left_event.y}. Arcs: {left_event.point_triple}")
        if right_event is not None:
            Tell.print(verbose, f"Right circle event created for {right_event.y}. Arcs: {right_event.point_triple}")

        return left_event, right_event

    @staticmethod
    def update_breakpoints(root, sweep_line, arc_node, predecessor, successor):

        # If the arc node is a left child, then its parent is the node with right_breakpoint
        if arc_node.is_left_child():

            # Replace the right breakpoint by the right node
            root = arc_node.parent.replace_leaf(arc_node.parent.right, root)

            # Mark the right breakpoint as removed and right breakpoint
            removed = arc_node.parent.data
            right = removed

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

            # Mark this breakpoint as updated and left breakpoint
            updated = breakpoint.data if breakpoint is not None else None
            left = updated

        # If the arc node is a right child, then its parent is the breakpoint on the left
        else:

            # Replace the left breakpoint by the left node
            root = arc_node.parent.replace_leaf(arc_node.parent.left, root)

            # Mark the left breakpoint as removed
            removed = arc_node.parent.data
            left = removed

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

            # Mark this breakpoint as updated and right breakpoint
            updated = breakpoint.data if breakpoint is not None else None
            right = updated

        return root, updated, removed, left, right
