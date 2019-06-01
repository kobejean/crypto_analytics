import pandas as pd
from abc import ABC, abstractmethod
from crypto_analytics.types  import Interval

class DataSource(ABC):
    """ An abstract base class for all data sources """

    def __init__(self):
        self.data = None
        super().__init__()

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass

    # TODO: Depricate and let data_handler write files
    @abstractmethod
    def write(self, filepath: str):
        pass

    @abstractmethod
    def get_time(self):
        pass


class OHLCDataSource(DataSource):
    """ An abstract class for all OHLC data sources """
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


class OHLCVDataSource(OHLCDataSource):
    """ An abstract class for all OHLCV data sources """

    @abstractmethod
    def get_volume(self):
        pass
