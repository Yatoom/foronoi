import uuid
from graphviz import Digraph


class TreeVisualizer:

    def plot(self, node):
        dot = Digraph(comment='Binary Tree')
        self._plot(node, dot, None)
        return dot

    @staticmethod
    def _plot(node, dot, parent_id):
        id = str(uuid.uuid4())
        label = node.get_label()
        dot.node(id, label)

        # Check if parent is None
        if parent_id is not None:
            dot.edge(parent_id, id)

        if node.left is not None:
            TreeVisualizer._plot(node.left, dot, id)

        if node.right is not None:
            TreeVisualizer._plot(node.right, dot, id)