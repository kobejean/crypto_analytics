import pandas as  pd
import json
import krakenex
from typing import Dict, Any

from crypto_analytics.collection.data_source import FinancialDataSource
from crypto_analytics.types import Interval

class KrakenOHLC(FinancialDataSource):
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']

    def __init__(self, interval: Interval, pair: str, since: int = None):
        self.interval = interval
        self.pair = pair
        self.since = since
        super().__init__()

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

    # TODO: implement this getter method
    def get_open(self, interval: Interval):
        pass

    # TODO: implement this getter method
    def get_close(self, interval: Interval):
        pass

    # TODO: implement this getter method
    def get_high(self, interval: Interval):
        pass

    # TODO: implement this getter method
    def get_low(self, interval: Interval):
        pass

    # TODO: implement this getter method
    def get_volume(self, inteval: Interval):
        pass
