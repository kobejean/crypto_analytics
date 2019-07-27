import time, os
import pandas as pd
from abc import ABC, abstractmethod, abstractproperty
from typing import Optional

from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import SymbolPair
from crypto_analytics.utils.typing import RealNumber, coalesce
from crypto_analytics import utils

class DataSource(ABC):
    """ An abstract base class for all data sources """

    def __init__(self):
        self._data = None
        super().__init__()

    @property
    def data(self) -> Optional[pd.DataFrame]:
        return self._data

    @abstractmethod
    def fetch(self) -> pd.DataFrame:
        pass

    def write(self, filepath: str):
        if os.path.isfile(filepath):
            # concat current data if writing to an existing file
            self._data.to_csv(filepath, index=False, mode='a', header=False)
        else:
            self._data.to_csv(filepath, index=False)

    def validate(self):
        # check existance of data
        if self.data is None:
            raise ValueError('No data')
        # check type of data
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError('The data is not an instance of the pandas DataFrame type')



class TimeSeriesDataSource(DataSource):
    """ An abstract class for all time series data sources """
    def __init__(self, interval: Interval, rows: int):
        self._interval = interval
        self._rows = rows
        self._to_time: Optional[RealNumber] = None
        super().__init__()

    @property
    def interval(self) -> Interval:
        return self._interval

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def to_time(self) -> RealNumber:
        return coalesce(self._to_time, lambda: time.time())

    @to_time.setter
    def to_time(self, to_time: RealNumber):
        self._to_time = to_time

    @property
    def fetch_period(self) -> RealNumber:
        return self._interval.to_unix_time() * self.rows

    def validate(self):
        super().validate()
        # check row count of data
        if len(self.data.index) != self.rows:
            ValueError('Did not recieve the expected number of rows')

    @abstractproperty
    def time(self):
        pass


class OHLCDataSource(TimeSeriesDataSource):
    """ An abstract class for all OHLC data sources """
    def __init__(self, interval: Interval, pair: SymbolPair, rows: int):
        self.pair = pair
        super().__init__(interval, rows)

    @abstractproperty
    def open(self):
        pass

    @abstractproperty
    def close(self):
        pass

    @abstractproperty
    def high(self):
        pass

    @abstractproperty
    def low(self):
        pass


class OHLCVDataSource(OHLCDataSource):
    """ An abstract class for all OHLCV data sources """

    @abstractproperty
    def volume(self):
        pass
