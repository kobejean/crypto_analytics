from abc import abstractmethod
from .base import DataSource
from ...types import Interval

class CandlesDataSource(DataSource):

    def __init__(self, interval: Interval):
        self.interval = interval
        super().__init__()

    @abstractmethod
    def get_open(self):
        pass

    @abstractmethod
    def get_close(self):
        pass

    @abstractmethod
    def get_high(self):
        pass

    @abstractmethod
    def get_low(self):
        pass

    @abstractmethod
    def get_volume(self):
        pass
