from voronoi_diagram import Point


class HalfEdge:
    def __init__(self, origin=None, prev=None, next=None, twin=None, inner_point=None, incident_face=None):
        self.origin: Vertex = origin
        self.prev: "HalfEdge" = prev
        self.next: "HalfEdge" = next
        self.twin: "HalfEdge" = twin
        self.inner_point: Point = inner_point
        self.incident_face: Face = incident_face


class Vertex:
    def __init__(self, x=None, y=None, incident_edge=None, attributes=None):
        self.x = x
        self.y = y
        self.incident_edge = incident_edge
        self.attributes = attributes


class Face:
    def __init__(self, outer_component=None, inner_components=None, atttributes=None):
        # Half edge of outer cycle
        self.outer_component: HalfEdge = outer_component

        # List of half-edges for the inner cycles bounding the face
        self.inner_components: list = inner_components or []

        self.attributes = atttributes
