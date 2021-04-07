from abc import ABC

from foronoi.algorithm import Algorithm
from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
import matplotlib.pyplot as plt

from foronoi.visualization.visualizer import Visualizer, Presets


class VoronoiObserver(Observer, ABC):
    def __init__(self, visualize_steps=True, visualize_before_clipping=False, visualize_result=True, callback=None,
                 figsize=(8, 8), canvas_offset=1, settings=None):
        """
        Observers the state of the algorithm (:class:`foronoi.algorithm.Algorithm`) and visualizes
        the result using the Visualizer (:class:`foronoi.visualization.visualizer.Visualizer`).

        Parameters
        ----------
        visualize_steps: bool
            Visualize all individual steps
        visualize_before_clipping: bool
            Visualize the result before the edges are clipped
        visualize_result: bool
            Visualize the final result
        callback: function
            By default, the VoronoiObserver shows or prints the result when
            `text_based` is true. When a callback function is given, either the GraphViz diagram or the text-string
            is passed to the callback.
        figsize: (float, float)
            Window size in inches
        canvas_offset: float
            The space around the bounding object
        settings: dict
            Visualizer settings to override the default presets used by the VoronoiObserver

        Examples
        --------
        >>> from foronoi import Voronoi, VoronoiObserver, Polygon
        >>> points = [
        ...    (2.5, 2.5), (4, 7.5), (7.5, 2.5), (6, 7.5), (4, 4), (3, 3), (6, 3)
        ... ]
        >>> poly = Polygon(
        ...    [(2.5, 10), (5, 10), (10, 5), (10, 2.5), (5, 0), (2.5, 0), (0, 2.5), (0, 5)]
        ... )
        >>> v = Voronoi(poly)
        >>>
        >>> # Define callback and settings
        >>> def callback(observer, figure):
        ...    figure.savefig(f"output/voronoi/{observer.n_messages:02d}.png")
        >>> settings=dict(arc_labels=True, site_labels=True)
        >>>
        >>> # Attach observer
        >>> v.attach_observer(VoronoiObserver(callback=callback, settings=settings))
        >>>
        >>> # Start diagram creation
        >>> v.create_diagram(points)
        """
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
        """
        Send the updated state of the algorithm to the VoronoiObserver.

        Parameters
        ----------
        subject: Algorithm
            The algorithm to observe
        message: Message
            The message type
        """
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
