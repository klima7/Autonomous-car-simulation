from enum import Enum


class SignType(Enum):
    STOP = 0
    WALKWAY = 1
    ROUNDABOUT = 2
    PARKING = 3
    LIMIT = 4
    ONEWAY = 5
    DEADEND = 6
    TRAFFIC_LIGHTS = 7
    REVERSED = 8
    UNKNOWN = 9
