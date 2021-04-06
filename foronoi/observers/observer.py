from abc import ABC, abstractmethod

from foronoi.observers.message import Message


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject, message: Message, **kwargs) -> None:
        """
        Receive update from subject.
        """
        pass






