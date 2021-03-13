from abc import ABC

from voronoi.algorithm import Algorithm
from voronoi.beta.message import Message
from voronoi.beta.observer import Observer
from voronoi.beta.subject import Subject
from voronoi.beta import tree_visualizer


class TreeObserver(Observer, ABC):
    def __init__(self):
        pass

    def update(self, subject: Algorithm, message: Message, **kwargs):
        if message == Message.STEP_FINISHED:
            print(subject.beach_line)
            tree_visualizer.visualize(subject.beach_line)
