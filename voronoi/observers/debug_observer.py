from abc import ABC

from voronoi.observers.message import Message
from voronoi.observers.observer import Observer
from voronoi.observers.subject import Subject


class DebugObserver(Observer, ABC):
    def __init__(self, callback=None):
        self.callback = callback

    def update(self, subject: Subject, message: Message, **kwargs):
        if message == Message.DEBUG:
            if self.callback is not None:
                self.callback(kwargs['payload'])
            else:
                print(kwargs['payload'])
