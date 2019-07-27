import time, os
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional

from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import SymbolPair
from crypto_analytics.utils.typing import RealNumber, coalesce
from crypto_analytics import utils

class DataSource(ABC):
    """ An abstract base class for all data sources """

    def __init__(self):
        self.data = None
        super().__init__()

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass

    def write(self, filepath: str):
        if os.path.isfile('/path/to/file'):
            self.data.to_csv(filepath, index=False, mode='a', header=False)
        else:
            self.data.to_csv(filepath, index=False)

    @abstractmethod
    def get_time(self):
        pass


class TimeSeriesDataSource(DataSource):
    """ An abstract class for all time series data sources """
    def __init__(self, interval: Interval, rows: int):
        self.interval = interval
        self.rows = rows
        self.__to_time: Optional[RealNumber] = None
        super().__init__()

    def set_to_time(self, to_time: Optional[RealNumber]):
        self.__to_time = to_time

    def get_to_time(self) -> RealNumber:
        return coalesce(self.__to_time, lambda: time.time())


class OHLCDataSource(TimeSeriesDataSource):
    """ An abstract class for all OHLC data sources """
    def __init__(self, interval: Interval, pair: SymbolPair, rows: int):
        self.pair = pair
        super().__init__(interval, rows)

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
