from abc import ABC

from foronoi.algorithm import Algorithm
from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
import matplotlib.pyplot as plt

from foronoi.visualization.visualizer import Visualizer, Presets


class VoronoiObserver(Observer, ABC):
    def __init__(self, visualize_steps=True, visualize_before_clipping=False, visualize_result=True, callback=None,
                 figsize=(8, 8), canvas_offset=1, settings=None):
        self.canvas_offset = canvas_offset
        self.figsize = figsize
        self.visualize_steps = visualize_steps
        self.visualize_before_clipping = visualize_before_clipping
        self.visualize_result = visualize_result
        self.callback = callback or (lambda a, b: plt.show(block=True))
        self.n_messages = 0
        self.messages = []
        self.settings = settings or {}

    def update(self, subject: Algorithm, message: Message, **kwargs):

        if not isinstance(subject, Algorithm):
            return False

        if message == Message.STEP_FINISHED and self.visualize_steps:
            vis = Visualizer(subject, canvas_offset=self.canvas_offset)
            settings = Presets.construction
            settings.update(self.settings)
            assert subject.sweep_line == subject.event.yd
            result = vis.plot_all(**settings)
            plt.title(str(subject.event) + "\n")
        elif message == Message.SWEEP_FINISHED and self.visualize_before_clipping:
            vis = Visualizer(subject, canvas_offset=self.canvas_offset)
            settings = Presets.clipping
            settings.update(self.settings)
            result = vis.plot_all(**settings)
            plt.title("Sweep finished\n")
        elif message == Message.VORONOI_FINISHED and self.visualize_result:
            vis = Visualizer(subject, canvas_offset=self.canvas_offset)
            settings = Presets.final
            settings.update(self.settings)
            result = vis.plot_all(**settings)
            plt.title("Voronoi completed\n")

        else:
            return

        self.callback(self, result.get_canvas())
        self.n_messages += 1
        self.messages.append(message)
