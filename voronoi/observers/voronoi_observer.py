from abc import ABC

from voronoi.algorithm import Algorithm
from voronoi.observers.message import Message
from voronoi.observers.observer import Observer
from voronoi.observers.subject import Subject
from voronoi.graph.bounding_circle import BoundingCircle
from voronoi.visualization import vis
import matplotlib.pyplot as plt


class VoronoiObserver(Observer, ABC):
    def __init__(self, visualize_steps=False, visualize_before_clipping=False, visualize_result=True, callback=None):
        self.visualize_steps = visualize_steps
        self.visualize_before_clipping = visualize_before_clipping
        self.visualize_result = visualize_result
        self.callback = callback

    def update(self, subject: Subject, message: Message, **kwargs):
        if not isinstance(subject, Algorithm):
            return False

        if message == Message.STEP_FINISHED and self.visualize_steps:
            self.visualize(subject, y=subject.sweep_line, event_name=kwargs['event'], calc_cell_sizes=False)

        elif message == Message.SWEEP_FINISHED and self.visualize_before_clipping:
            self.visualize(subject, y=-1000, event_name="Before clipping", calc_cell_sizes=False)

        elif message == Message.VORONOI_FINISHED and self.visualize_result:
            # Bounding circle doesn't support this
            calc_cell_sizes = not isinstance(subject.bounding_poly, BoundingCircle)
            self.visualize(subject, y=-1000, event_name="Final result",
                           calc_cell_sizes=calc_cell_sizes)

    def visualize(self, subject, y, event_name, calc_cell_sizes):
        visualization = vis.visualize(y=y, current_event=event_name, bounding_poly=subject.bounding_poly,
                                      points=subject.points, vertices=subject.vertices, edges=subject.edges,
                                      arc_list=subject.arcs,
                                      event_queue=subject.event_queue, calc_cell_sizes=calc_cell_sizes)

        if self.callback is not None:
            self.callback(visualization)
        else:
            # visualization.show(block=True)
            plt.show()
