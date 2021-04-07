from abc import ABC

from foronoi.observers.message import Message
from foronoi.observers.observer import Observer
from foronoi.observers.subject import Subject


class DebugObserver(Observer, ABC):
    def __init__(self, callback=None):
        """
        Listens to debug messages.

        Parameters
        ----------
        callback: function
            By default, the DebugObserver prints the debug message. When a callback function is given, it will pass
            the debug message as string to the callback function.
        """
        self.callback = callback or (lambda _: print(_))

    def update(self, subject: Subject, message: Message, **kwargs):
        """
        Send the updated state of the algorithm to the VoronoiObserver.

        Parameters
        ----------
        subject: Algorithm
            The algorithm to observe
        message: Message
            The message type
        kwargs: dict
            Keyword arguments that include a payload-parameter of type str
        """
        if message == Message.DEBUG:
            self.callback(kwargs['payload'])
