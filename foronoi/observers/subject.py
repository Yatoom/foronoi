from foronoi.observers.observer import Observer


class Subject:
    def __init__(self):
        """
        An observable subject that you can attach observers to.
        """
        self._observers = []
        self._children = []
        self._root_sender = self
        self._child_sender = self

    def attach_observer(self, observer: Observer):
        """
        Attach an observer to the subject.

        Parameters
        ----------
        observer: Observer
            An observer to attach to this subject
        """
        self._observers.append(observer)
        self._update_children()
        return self

    def detach_observer(self, observer: Observer):
        """
        Detach an observer from the subject.

        Parameters
        ----------
        observer: Observer
            An observer to remove from this subject
        """
        self._observers.remove(observer)
        self._update_children()
        return self

    def notify_observers(self, message, **kwargs):
        """
        Notify all observers about an event.

        Parameters
        ----------
        message: Message
            The message type
        """
        for observer in self._observers:
            observer.update(self._root_sender, message, **kwargs)
        return self

    def get_observers(self):
        """
        Getter for observers
        """
        return self._observers

    def inherit_observers_from(self, parent):
        """
        Make this subject inherit observers from a parent.
        When the child sends an update to the observers, the parent will be passed as the sender.

        Parameters
        ----------
        parent: Subject
            The parent to inherit observers from
        """
        parent._add_child(self)
        self._root_sender = parent
        self._child_sender = self

    def _add_child(self, child):
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
