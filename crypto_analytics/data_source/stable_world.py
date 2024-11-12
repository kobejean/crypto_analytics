import pandas as pd
import numpy as np
from typing import Dict, Union, Optional, cast

from crypto_analytics.data_source import OHLCVDataSource
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair, StableWorldSymbolPairConverter
from crypto_analytics import utils

class StableWorldOHLCV(OHLCVDataSource):
    max_rows = 719
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    # TODO: define appropriate dtypes
    dtypes = {'time': np.int64, 'open': object, 'high': object, 'low': object, 'close': object, 'vwap': object, 'volume': object, 'count': np.int64 }

    dollar_val = {
        Symbol.BITCOIN: 0.000013,
        Symbol.USD: 1.0,
        Symbol.JPY: 152.49,
        Symbol.VND: 25_274.99,
    }

    def __init__(self, interval: Interval, pair: SymbolPair, rows: Optional[int] = None):
        super().__init__(interval, pair, rows)
        self._interval= interval
        self._pair = pair
        self._converted_pair = StableWorldSymbolPairConverter.from_pair(self.pair)

    def fetch(self) -> pd.DataFrame:
        value = self.dollar_val[self._pair.tsym] / self.dollar_val[self._pair.fsym]

        data_array = [[self._interval.unix*t] + [value]*4 + [0]*3 for t in range(self.rows)]
        data = pd.DataFrame(data_array, columns=StableWorldOHLCV.columns)
        data = data.head(self.rows)
        data = data.astype(StableWorldOHLCV.dtypes)

        return self.data

    @property
    def time(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['time']

    @property
    def open(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['open']

    @property
    def close(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['close']

    @property
    def high(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['high']

    @property
    def low(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['low']

    @property
    def volume(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['volume']

