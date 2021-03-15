from abc import ABC

from voronoi.algorithm import Algorithm
from voronoi.observers.message import Message
from voronoi.observers.observer import Observer
import matplotlib.pyplot as plt

from voronoi.visualization.visualizer import Visualizer


class VoronoiObserver(Observer, ABC):
    def __init__(self, visualize_steps=False, visualize_before_clipping=False, visualize_result=True, callback=None,
                 figsize=(8, 8), canvas_offset=5):
        self.canvas_offset = canvas_offset
        self.figsize = figsize
        self.visualize_steps = visualize_steps
        self.visualize_before_clipping = visualize_before_clipping
        self.visualize_result = visualize_result
        self.callback = callback or (lambda _: plt.show(block=True))

    def update(self, subject: Algorithm, message: Message, **kwargs):

        if not isinstance(subject, Algorithm):
            return False

        if message == Message.STEP_FINISHED and self.visualize_steps:
            vis = Visualizer(subject.bounding_poly, canvas_offset=self.canvas_offset)
            result = vis.plot_all(subject, outgoing_edges=False)
            plt.title(str(kwargs['event']))
        elif message == Message.SWEEP_FINISHED and self.visualize_before_clipping:
            vis = Visualizer(subject.bounding_poly, canvas_offset=self.canvas_offset)
            result = vis.plot_all(subject, events=False, beachline=False, outgoing_edges=False)
            plt.title("Sweep finished")
        elif message == Message.VORONOI_FINISHED and self.visualize_result:
            vis = Visualizer(subject.bounding_poly, canvas_offset=self.canvas_offset)
            result = vis.plot_all(subject, events=False, beachline=False, outgoing_edges=False)
            plt.title("Voronoi completed")

        else:
            return

        self.callback(result)
