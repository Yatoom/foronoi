from abc import ABC

from voronoi.observers.message import Message
from voronoi.observers.observer import Observer
from voronoi.observers.subject import Subject


class DebugObserver(Observer, ABC):
    def __init__(self, callback=None):
        self.callback = callback or (lambda _: print(_))

    def update(self, subject: Subject, message: Message, **kwargs):
        if message == Message.DEBUG:
            self.callback(kwargs['payload'])
