from enum import Enum


class Message(Enum):
    """
    Enum class for message types.

    Attributes
    ----------
    STEP_FINISHED
        Indicates that the algorithm processed one event
    SWEEP_FINISHED
        Indicates that the sweep line algorithm is finished
    VORONOI_FINISHED
        Indicates that the voronoi diagram is clipped and cleaned
    DEBUG
        Indicates that this message is a debugging-message
    """
    STEP_FINISHED = 0
    SWEEP_FINISHED = 1
    VORONOI_FINISHED = 2
    DEBUG = 3
