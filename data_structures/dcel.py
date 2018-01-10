class HalfEdge:
    origin: Vertex = None
    prev = None
    next = None
    twin = None
    incident_face = None


class Vertex:
    coordinates = None
    incident_edge = None
    attributes = None


class Face:
    # Half edge of outer cycle
    outer_component: HalfEdge = None

    # List of half-edges for the inner cycles bounding the face
    inner_components: list = []

    attributes = None