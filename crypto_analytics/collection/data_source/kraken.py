import pandas as  pd
import json
import krakenex
from typing import Dict, Any

from .candles import CandlesDataSource
from ...types import Interval

class KrakenCandles(CandlesDataSource):
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']

    def __init__(self, interval: Interval, pair: str, since: int = None):
        self.pair = pair
        self.since = since
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

        kraken = krakenex.API()

        parameters = {
            'pair': self.pair,
            'interval': interval_int,
        }
        if self.since:
            parameters['since'] = self.since

        kraken = krakenex.API()
        response = kraken.query_public('OHLC', data = parameters)
        data = response.get('result', {}).get(self.pair, {})
        self.data = pd.DataFrame(data, columns=self.columns)
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
