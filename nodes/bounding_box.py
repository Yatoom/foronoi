from enum import Enum

from nodes.diagram import Vertex, HalfEdge
from nodes.point import Point


class BoundingBox:
    def __init__(self, left_x, right_x, bottom_y, top_y):
        self.left = left_x
        self.right = right_x
        self.bottom = bottom_y
        self.top = top_y

    def create_box(self, edges, vertices, genesis_point):
        edges, bounding_vertices = self.finish_edges(edges, self)
        edges, bounding_vertices = self.finish_bounding_box(edges, self, bounding_vertices, genesis_point)
        all_vertices = vertices + bounding_vertices
        return edges, all_vertices

    @staticmethod
    def finish_edges(edges, bounding_box):

        bounding_vertices = {
            Box.TOP: [],
            Box.RIGHT: [],
            Box.BOTTOM: [],
            Box.LEFT: []
        }

        for edge in edges:
            if edge.get_origin() is None or not BoundingBox.is_inside_box(edge.get_origin(), bounding_box):
                x, y, wall = BoundingBox.finish_edge(edge, bounding_box)
                v = Vertex(point=Point(x, y))
                v.incident_edges.append(edge)
                edge.origin = v
                bounding_vertices[wall].append(v)

            if edge.twin.get_origin() is None or not BoundingBox.is_inside_box(edge.get_origin(), bounding_box):
                x, y, wall = BoundingBox.finish_edge(edge.twin, bounding_box)
                v = Vertex(point=Point(x, y))
                v.incident_edges.append(edge.twin)
                edge.twin.origin = v
                bounding_vertices[wall].append(v)

        return edges, bounding_vertices

    @staticmethod
    def is_inside_box(point, bounding_box):
        inside_x = bounding_box.left <= point.x <= bounding_box.right
        inside_y = bounding_box.bottom <= point.y <= bounding_box.top
        return inside_x and inside_y

    @staticmethod
    def finish_edge(edge, bounding_box):

        # Start should be a breakpoint
        start = edge.get_origin(y=bounding_box.bottom - bounding_box.top, bounding_box=bounding_box)

        # End should be a vertex
        end = edge.twin.get_origin(y=bounding_box.bottom**2 - bounding_box.top, bounding_box=bounding_box)

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
        time_x = dist_x / speed_x if speed_x != 0 else float('inf')
        time_y = dist_y / speed_y if speed_y != 0 else float('inf')

        if time_x < time_y:
            slope = (start.y - end.y) / (start.x - end.x)
            wall = Box.RIGHT if right else Box.LEFT
            return x, slope * (x - start.x) + start.y, wall

        slope = (start.x - end.x) / (start.y - end.y)
        wall = Box.TOP if up else Box.BOTTOM
        return slope * (y - start.y) + start.x, y, wall

    @staticmethod
    def finish_bounding_box(edges, bounding_box, bounding_vertices, genesis_point):

        # Create corner vertices
        top_left = Vertex(point=Point(bounding_box.left, bounding_box.top))
        top_right = Vertex(point=Point(bounding_box.right, bounding_box.top))
        bottom_right = Vertex(point=Point(bounding_box.right, bounding_box.bottom))
        bottom_left = Vertex(point=Point(bounding_box.left, bounding_box.bottom))

        # Top wall
        bounding_vertices[Box.TOP].append(top_left)
        bounding_box_top = sorted(bounding_vertices[Box.TOP], key=lambda vertex: vertex.position.x)

        # Right wall
        bounding_vertices[Box.RIGHT].append(top_right)
        bounding_box_right = sorted(bounding_vertices[Box.RIGHT], key=lambda vertex: - vertex.position.y)

        # Bottom wall
        bounding_vertices[Box.BOTTOM].append(bottom_right)
        bounding_box_bottom = sorted(bounding_vertices[Box.BOTTOM], key=lambda vertex: - vertex.position.x)

        # Left wall
        bounding_vertices[Box.LEFT].append(bottom_left)
        bounding_vertices[Box.LEFT].append(top_left)
        bounding_box_left = sorted(bounding_vertices[Box.LEFT], key=lambda vertex: vertex.position.y)

        vertices = bounding_box_top + bounding_box_right + bounding_box_bottom + bounding_box_left

        next_incident_point = genesis_point
        previous_edge = None
        for index in range(0, len(vertices) - 1):

            # Get start and end vertices
            start = vertices[index]
            end = vertices[index + 1]

            # Set the incident point to the last retrieved next incident point
            incident_point = next_incident_point

            # If the vertex has edges connected, we determine the current and the next incident point
            if len(end.incident_edges) > 0:
                edge = end.incident_edges[0]
                incident_point = edge.incident_point
                next_incident_point = edge.twin.incident_point

            # Create the edge
            edge = HalfEdge(incident_point, origin=start, twin=HalfEdge(None, origin=end))
            start.incident_edges.append(edge)
            end.incident_edges.append(edge.twin)

            # Connect edges
            if len(end.incident_edges) > 0:
                edge.set_next(end.incident_edges[0])

            # Connect to incoming edge, or previous edge
            if len(start.incident_edges) > 0:
                start.incident_edges[0].twin.set_next(edge)
            elif previous_edge is not None:
                previous_edge.set_next(edge)

            # Add the edge to the list
            edges.append(edge)

            # Set previous edge
            previous_edge = edge

        return edges, vertices


class Box(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
