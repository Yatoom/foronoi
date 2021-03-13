from voronoi.beta.observer import Observer


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        self._observers.remove(observer)

    def notify(self, message, **kwargs) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self, message, **kwargs)
