from enum import Enum


class Message(Enum):
    STEP_FINISHED = 0
    SWEEP_FINISHED = 1
    VORONOI_FINISHED = 2
    CIRCLE_EVENT = 3
    SITE_EVENT = 4
    DEBUG = 5