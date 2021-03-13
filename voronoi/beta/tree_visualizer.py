import uuid
from graphviz import Digraph


def _visualize(node, dot, parent_id):
    id = str(uuid.uuid4())
    label = node.get_label()
    dot.node(id, label)

    # Check if parent is None
    if parent_id is not None:
        dot.edge(parent_id, id)

    if node.left is not None:
        _visualize(node.left, dot, id)

    if node.right is not None:
        _visualize(node.right, dot, id)


def visualize(node):
    dot = Digraph(comment='Binary Tree')
    _visualize(node, dot, None)
    dot.render('test-output/round-table.gv', view=True)