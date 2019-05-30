""" Contains interval definitions """
from enum import Enum

class Interval(Enum):
    MINUTE = 'minute'
    HOURLY = 'hourly'
    DAILY = 'daily'

    def to_unix_time(self):
        if self == Interval.MINUTE:
            return 60
        elif self == Interval.HOURLY:
            return 60*60
        elif self == Interval.DAILY:
            return 60*60*24
        return None
