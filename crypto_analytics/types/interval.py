""" Contains interval definitions """
from enum import Enum

class Interval(Enum):
    SECOND = 'SECOND'
    MINUTE = 'MINUTE'
    HOUR = 'HOUR'
    DAY = 'DAY'

    @property
    def unix(self) -> int:
        switch = {
            Interval.SECOND: 1,
            Interval.MINUTE: 60,
            Interval.HOUR: 60*60,
            Interval.DAY: 60*60*24,
        }
        return switch[self]
