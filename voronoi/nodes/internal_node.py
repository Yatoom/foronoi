from voronoi.tree.smart_node import SmartNode


class InternalNode(SmartNode):
    def __init__(self, data: "Breakpoint"):
        super().__init__(data)

    def __repr__(self):
        return f"Internal({self.data}, left={self.left}, right={self.right})"

    def get_key(self, sweep_line=None):
        return self.data.get_intersection(sweep_line).x

    def get_value(self, **kwargs):
        return self.data

    def get_label(self):
        return f"{self.data.breakpoint[0].name}{self.data.breakpoint[1].name}"
