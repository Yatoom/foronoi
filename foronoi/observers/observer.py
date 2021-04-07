from abc import ABC, abstractmethod

from foronoi.observers.message import Message


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject, message: Message, **kwargs) -> None:
        """

        Parameters
        ----------
        subject: Subject
            The sender of the update
        message: Message
            The message type
        kwargs: dict
            Any additional keyword arguments
        """
        pass






