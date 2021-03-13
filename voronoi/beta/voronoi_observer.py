from abc import ABC

from voronoi.algorithm import Algorithm
from voronoi.beta.message import Message
from voronoi.beta.observer import Observer
from voronoi.beta.subject import Subject
from voronoi.graph.bounding_circle import BoundingCircle
from voronoi.visualization import vis
import matplotlib.pyplot as plt


class VoronoiObserver(Observer, ABC):
    def __init__(self, visualize_steps=False, visualize_before_clipping=False, visualize_result=False, callback=None):
        self.visualize_steps = visualize_steps
        self.visualize_before_clipping = visualize_before_clipping
        self.visualize_result = visualize_result
        self.callback = callback

    def update(self, subject: Subject, message: Message, **kwargs):
        if not isinstance(subject, Algorithm):
            return False

        print(message)

        if message == Message.STEP_FINISHED and self.visualize_steps:
            VoronoiObserver.visualize(subject, y=subject.sweep_line, event_name=kwargs['event'], calc_cell_sizes=False,
                                      callback=self.callback)

        elif message == Message.SWEEP_FINISHED and self.visualize_before_clipping:
            VoronoiObserver.visualize(subject, y=-1000, event_name="Before clipping", calc_cell_sizes=False,
                                      callback=self.callback)

        elif message == Message.VORONOI_FINISHED and self.visualize_result:
            VoronoiObserver.visualize(subject, y=-1000, event_name="Final result",
                                      calc_cell_sizes=not isinstance(subject.bounding_poly, BoundingCircle),
                                      callback=self.callback)

    @staticmethod
    def visualize(subject, y, event_name, calc_cell_sizes, callback=None):
        visualization = vis.visualize(y=y, current_event=event_name, bounding_poly=subject.bounding_poly,
                                      points=subject.points, vertices=subject.vertices, edges=subject.edges,
                                      arc_list=subject.arcs,
                                      event_queue=subject.event_queue, calc_cell_sizes=calc_cell_sizes)

        if callback is not None:
            callback(visualization)
        else:
            # visualization.show(block=True)
            plt.show()
