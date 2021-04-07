from abc import ABC

from foronoi.algorithm import Algorithm
from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
import uuid
from graphviz import Digraph


class TreeObserver(Observer, ABC):
    def __init__(self, visualize_steps=True, visualize_result=True, text_based=False, callback=None):
        """
        Observers the state of the status tree (:attr:`foronoi.algorithm.Algorithm.status_tree`) and visualizes
        the result using GraphViz.

        Parameters
        ----------
        visualize_steps: bool
            Visualize all individual steps
        visualize_result: bool
            Visualize the final result
        text_based: bool
            Visualize the tree using plain text instead of GraphViz
        callback: function
            By default, the TreeObserver renders and shows the result in a window, or prints the result when
            `text_based` is true. When a callback function is given, either the GraphViz diagram or the text-string
            is passed to the callback.

        Examples
        --------
        >>> from foronoi import Voronoi, TreeObserver, Polygon
        >>> points = [
        ...    (2.5, 2.5), (4, 7.5), (7.5, 2.5), (6, 7.5), (4, 4), (3, 3), (6, 3)
        ... ]
        >>> poly = Polygon(
        ...    [(2.5, 10), (5, 10), (10, 5), (10, 2.5), (5, 0), (2.5, 0), (0, 2.5), (0, 5)]
        ... )
        >>> v = Voronoi(poly)
        >>>
        >>> # Define callback
        >>> def callback(observer, dot):
        ...    dot.render(f"output/tree/{observer.n_messages:02d}")
        >>>
        >>> # Attach observer
        >>> v.attach_observer(TreeObserver(callback=callback))
        >>>
        >>> # Start diagram creation
        >>> v.create_diagram(points)
        """

        self.text_based = text_based
        self.visualize_steps = visualize_steps
        self.visualize_result = visualize_result
        self.callback = callback
        self.n_messages = 0
        self.messages = []

    def update(self, subject: Algorithm, message: Message, **kwargs):
        """
        Send the updated state of the algorithm to the TreeObserver.

        Parameters
        ----------
        subject: Algorithm
            The algorithm to observe
        message: Message
            The message type
        """
        if (message == Message.STEP_FINISHED and self.visualize_steps) or \
           (message == Message.VORONOI_FINISHED and self.visualize_result and not self.visualize_steps):
            if self.text_based:
                visualized_in_text = subject.status_tree.visualize()
                if self.callback is not None:
                    self.callback(visualized_in_text)
                else:
                    print(visualized_in_text)
            else:
                self._create_graph(subject.status_tree)
            self.n_messages += 1
            self.messages.append(message)

    def _create_graph(self, node):
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
