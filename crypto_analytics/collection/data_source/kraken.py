import pandas as  pd
import time
import requests
from typing import Dict

from crypto_analytics.collection.data_source import OHLCVDataSource
from crypto_analytics.types import Interval

class KrakenOHLCV(OHLCVDataSource):
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']

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

        interval_duration = self.interval.to_unix_time()
        last_time = time.time() if not self.last_time else last_time
        since = (last_time//interval_duration - self.rows - 1) * interval_duration
        parameters: Dict[str, Union[int, str]] = {
            'pair': self.pair,
            'interval': interval_int,
            'since': since,
        }

        response = requests.get(endpoint, params=parameters)
        response.raise_for_status()

        self.data = self.__data_frame_from_response(response)
        return self.data


    def write(self, filepath: str):
        self.data.to_csv(filepath)

    def get_time(self):
        return self.data['time']

    def get_open(self):
        return self.data['open']

    def get_close(self):
        return self.data['close']

    def get_high(self):
        return self.data['high']

    def get_low(self):
        return self.data['low']

    def get_volume(self):
        return self.data['volume']

    def __data_frame_from_response(self, response):
        tabular_data = response.json().get('result', {}).get(self.pair, {})
        df = pd.DataFrame(tabular_data, columns=self.columns).head(self.rows)

        self.__validate_data_frame(df, response)
        return df

    def __validate_data_frame(self, df, response):
        last_time_valid = response.json().get('result', {}).get('last')
        last_time = df.at[df.index[-1], 'time']

        print('last_time', last_time_valid, last_time)
        if df.shape[0] < self.rows:
            raise ValueError('Did not recieve enough rows')
        elif last_time > last_time_valid:
            raise ValueError('Last candle was not completed')
