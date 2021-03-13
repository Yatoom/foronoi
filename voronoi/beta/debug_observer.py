from abc import ABC

from voronoi.beta.message import Message
from voronoi.beta.observer import Observer
from voronoi.beta.subject import Subject


class DebugObserver(Observer, ABC):
    def __init__(self):
        pass

    def update(self, subject: Subject, message: Message, **kwargs):
        if message == Message.DEBUG:
            print(kwargs['payload'])
