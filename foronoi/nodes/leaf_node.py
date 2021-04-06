from foronoi.nodes import Arc
from foronoi.tree.node import Node


class LeafNode(Node):
    def __init__(self, data: "Arc"):
        super().__init__(data)

    def __repr__(self):
        return f"Leaf({self.data}, left={self.left}, right={self.right})"

    def get_key(self, sweep_line=None):
        return self.data.origin.xd

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data.origin.name}"


