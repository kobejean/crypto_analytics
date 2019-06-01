from abc import abstractmethod
from crypto_analytics.collection.data_source import DataSource
from crypto_analytics.types import Interval

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
