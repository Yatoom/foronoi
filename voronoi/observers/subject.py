from voronoi.observers.observer import Observer


class Subject:
    def __init__(self):
        self._observers = []
        self._children = []

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        self._observers.append(observer)
        self.update_children()

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        self._observers.remove(observer)
        self.update_children()

    def notify(self, message, **kwargs) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self, message, **kwargs)

    def get_observers(self):
        """
        Getter for observers
        """
        return self._observers

    def update_children(self):
        """
        Send the observers to the children
        """
        for child in self._children:
            child._observers = self.get_observers()

    def add_child(self, child):
        """
        Add child
        """
        self._children.append(child)

    def inherit_observers_from(self, subject):
        """
        Make this subject inherit observers from a parent
        """
        subject.add_child(self)
