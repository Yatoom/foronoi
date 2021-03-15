from voronoi.observers.observer import Observer


class Subject:
    def __init__(self):
        self._observers = []
        self._children = []
        self._root_sender = self
        self._child_sender = self

    def attach_observer(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        self._observers.append(observer)
        self._update_children()

    def detach_observer(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        self._observers.remove(observer)
        self._update_children()

    def notify_observers(self, message, **kwargs) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self._root_sender, message, **kwargs)

    def get_observers(self):
        """
        Getter for observers
        """
        return self._observers

    def inherit_observers_from(self, parent):
        """
        Make this subject inherit observers from a parent.
        Set the sender to self.
        """
        parent.add_child(self)
        self._root_sender = parent
        self._child_sender = self

    def add_child(self, child):
        """
        Add child
        """
        self._children.append(child)

    def _update_children(self):
        """
        Send the observers to the children
        """
        for child in self._children:
            child._observers = self.get_observers()
