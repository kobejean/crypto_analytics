import pandas as pd
import numpy as np
import requests
from typing import Dict, Union, Optional

from crypto_analytics.collection.data_source import OHLCVDataSource
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import SymbolPair, KrakenSymbolPairConverter
from crypto_analytics import utils

class KrakenOHLCV(OHLCVDataSource):
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    # TODO: define appropriate dtypes
    dtypes = {'time': np.int64, 'open': object, 'high': object, 'low': object, 'close': object, 'vwap': object, 'volume': object, 'count': np.int64 }

    def __init__(self, interval: Interval, pair: SymbolPair, rows: int):
        super().__init__(interval, pair, rows)
        self._last_valid_time: Optional[int] = None

    def fetch(self) -> pd.DataFrame:
        interval_ints = {
            Interval.MINUTE: 1,
            Interval.HOUR: 60,
            Interval.DAY: 60*24,
        }
        interval_int = interval_ints.get(self.interval)

        if not interval_int:
            raise ValueError('Interval must be daily, hourly or minute')

        endpoint = 'https://api.kraken.com/0/public/OHLC'

        converted_pair = KrakenSymbolPairConverter.from_pair(self.pair)
        interval_duration = self.interval.to_unix_time()
        candle_time = utils.time.candle_time(self.interval, self.to_time)
        since = candle_time - self.rows * interval_duration
        parameters: Dict[str, Union[int, str]] = {
            'pair': converted_pair,
            'interval': interval_int,
            'since': since,
        }

        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()

        data_array = response.json().get('result', {}).get(converted_pair, {})
        data = pd.DataFrame(data_array, columns=KrakenOHLCV.columns)
        data = data.head(self.rows).astype(KrakenOHLCV.dtypes)

        self._last_valid_time = int(response.json().get('result', {}).get('last'))
        self._data = data

        self.validate()
        return self.data

    @property
    def time(self) -> pd.Series:
        return self._data['time']

    @property
    def open(self) -> pd.Series:
        return self._data['open']

    @property
    def close(self) -> pd.Series:
        return self._data['close']

    @property
    def high(self) -> pd.Series:
        return self._data['high']

    @property
    def low(self) -> pd.Series:
        return self._data['low']

    @property
    def volume(self) -> pd.Series:
        return self._data['volume']

    def validate(self):
        super().validate()
        last_time_data = self._data.at[self.data.index[-1], 'time']

        if last_time_data > self._last_valid_time:
            raise ValueError('Last candle was not completed')
