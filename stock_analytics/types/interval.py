""" Contains interval definitions """
from enum import Enum

class Interval(Enum):
    MINUTE = 'minute'
    HOURLY = 'hourly'
    DAILY = 'daily'
