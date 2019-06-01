from abc import abstractmethod
from .base import DataSource
from ...types import Interval 

class FinancialDataSource(DataSource):
    
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_open(self, interval: Interval):
        pass

    @abstractmethod
    def get_close(self, interval: Interval):
        pass

    @abstractmethod
    def get_high(self, interval: Interval):
        pass

    @abstractmethod
    def get_low(self, interval: Interval):
        pass

    @abstractmethod
    def get_volume(self, interval: Interval):
        pass
