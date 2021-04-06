from abc import ABC

from foronoi.algorithm import Algorithm
from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
import uuid
from graphviz import Digraph


class TreeObserver(Observer, ABC):
    def __init__(self, visualize_steps=True, visualize_before_clipping=False, visualize_result=True, text_based=False, callback=None):
        self.text_based = text_based
        self.visualize_steps = visualize_steps
        self.visualize_before_clipping = visualize_before_clipping
        self.visualize_result = visualize_result
        self.callback = callback
        self.n_messages = 0
        self.messages = []

    def update(self, subject: Algorithm, message: Message, **kwargs):
        if (message == Message.STEP_FINISHED and self.visualize_steps) or \
           (message == Message.VORONOI_FINISHED and self.visualize_result) or \
           (message == Message.SWEEP_FINISHED and self.visualize_before_clipping):
            if self.text_based:
                visualized_in_text = subject.status_tree.visualize()
                if self.callback is not None:
                    self.callback(visualized_in_text)
                else:
                    print(visualized_in_text)
            else:
                self.visualize(subject.status_tree)
            self.n_messages += 1
            self.messages.append(message)

    def visualize(self, node):
        dot = Digraph(comment='Binary Tree', format="png")
        self._visualize(node, dot, None)

        if self.callback is not None:
            self.callback(self, dot)
        else:
            dot.render('tree/tree.gv', view=True)

    @staticmethod
    def _visualize(node, dot, parent_id):
        id = str(uuid.uuid4())
        label = node.get_label()
        dot.node(id, label)

        # Check if parent is None
        if parent_id is not None:
            dot.edge(parent_id, id)

        if node.left is not None:
            TreeObserver._visualize(node.left, dot, id)

        if node.right is not None:
            TreeObserver._visualize(node.right, dot, id)
