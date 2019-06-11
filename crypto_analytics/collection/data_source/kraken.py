import pandas as pd
import numpy as np
import time
import requests
from typing import Dict

from crypto_analytics.collection.data_source import OHLCVDataSource
from crypto_analytics.types import Interval

class KrakenOHLCV(OHLCVDataSource):
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    # TODO: define appropriate dtypes
    dtypes = {'time': np.int64, 'open': object, 'high': object, 'low': object, 'close': object, 'vwap': object, 'volume': object, 'count': np.int64 }

    def __init__(self, interval: Interval, pair: str, rows: int, last_time: int = None):
        self.pair = pair
        self.rows = rows
        self.last_time = last_time
        super().__init__(interval)

    def fetch(self) -> pd.DataFrame:
        interval_ints = {
            Interval.MINUTE: 1,
            Interval.HOURLY: 60,
            Interval.DAILY: 60*24,
        }
        interval_int = interval_ints.get(self.interval)

        if not interval_int:
            raise ValueError('Interval must be daily, hourly or minute')

        endpoint = 'https://api.kraken.com/0/public/OHLC'

        last_time = time.time() if not self.last_time else self.last_time
        interval_duration = self.interval.to_unix_time()
        since = (last_time//interval_duration - self.rows - 1) * interval_duration
        parameters: Dict[str, Union[int, str]] = {
            'pair': self.pair,
            'interval': interval_int,
            'since': since,
        }

        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()

        data_array = response.json().get('result', {}).get(self.pair.upper(), {})
        data = pd.DataFrame(data_array, columns=KrakenOHLCV.columns)
        data = data.head(self.rows).astype(KrakenOHLCV.dtypes)

        self.__validate_data(data, response)

        self.data = data
        return self.data


    def write(self, filepath: str):
        self.data.to_csv(filepath, index=False)

    def get_time(self) -> pd.Series:
        return self.data['time']

    def get_open(self) -> pd.Series:
        return self.data['open']

    def get_close(self) -> pd.Series:
        return self.data['close']

    def get_high(self) -> pd.Series:
        return self.data['high']

    def get_low(self) -> pd.Series:
        return self.data['low']

    def get_volume(self) -> pd.Series:
        return self.data['volume']

    def __validate_data(self, data: pd.DataFrame, response: requests.Response):
        # result.last is the field that tells us the last valid timestamp
        last_time_valid = response.json().get('result', {}).get('last')
        last_time_data = data.at[data.index[-1], 'time']

        if data.shape[0] < self.rows:
            raise ValueError('Did not recieve enough rows')
        elif last_time_data > last_time_valid:
            raise ValueError('Last candle was not completed')
