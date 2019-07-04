""" Contains interval definitions """
from enum import Enum

class Interval(Enum):
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'

    def to_unix_time(self) -> int:
        switch = {
            Interval.MINUTE: 60,
            Interval.HOUR: 60*60,
            Interval.DAY: 60*60*24,
        }
        return switch[self]
