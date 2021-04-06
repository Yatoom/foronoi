from abc import ABC

from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
from foronoi.observers.subject import Subject


class DebugObserver(Observer, ABC):
    def __init__(self, callback=None):
        self.callback = callback or (lambda _: print(_))

    def update(self, subject: Subject, message: Message, **kwargs):
        if message == Message.DEBUG:
            self.callback(kwargs['payload'])
