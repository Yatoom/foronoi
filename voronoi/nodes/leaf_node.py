from voronoi.nodes import Arc
from voronoi.tree.smart_node import SmartNode


class LeafNode(SmartNode):
    def __init__(self, data: "Arc"):
        super().__init__(data)

    def __repr__(self):
        return f"Leaf({self.data}, left={self.left}, right={self.right})"

    def get_key(self, sweep_line=None):
        return self.data.origin.x

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data.origin.name}"


