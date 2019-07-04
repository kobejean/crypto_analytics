""" Contains interval definitions """
from enum import Enum

class Interval(Enum):
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'

    def to_unix_time(self):
        if self == Interval.MINUTE:
            return 60
        elif self == Interval.HOUR:
            return 60*60
        elif self == Interval.DAY:
            return 60*60*24
        return None
