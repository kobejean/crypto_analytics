import pandas as pd
import time
import json
import requests
from typing import Dict, Union

from crypto_analytics.collection.data_source import OHLCVDataSource
from crypto_analytics.types  import Interval
from crypto_analytics.types.symbol import SymbolPair, CryptoCompareSymbolPairConverter

class CryptoCompareOHLCV(OHLCVDataSource):
    endpoints = {
        Interval.MINUTE: 'data/histominute',
        Interval.HOURLY: 'data/histohour',
        Interval.DAILY: 'data/histoday',
    }

    def __init__(self, interval: Interval, pair: SymbolPair, rows: int, last_time: int = None):
        self.__prevalidate(interval, pair, rows)

        self.interval = interval
        self.pair = pair
        self.rows = rows
        self.last_time = last_time
        super().__init__(interval)

    def fetch(self) -> pd.DataFrame:
        endpoint = type(self).endpoints.get(self.interval)
        url = 'https://min-api.cryptocompare.com/{}'.format(endpoint)

        converted_pair = CryptoCompareSymbolPairConverter.from_pair(self.pair)
        limit = self.rows - 1
        interval_duration = self.interval.to_unix_time()
        last_time = time.time() if not self.last_time else self.last_time
        last_time = int((last_time//interval_duration - 1) * interval_duration)

        parameters: Dict[str, Union[int, str]] = {
            'fsym': converted_pair.fsym,
            'tsym': converted_pair.tsym,
            'limit': limit,
            'toTs': last_time
        }
        response = requests.get(url, params=parameters)
        response.raise_for_status()

        data = response.json()
        self.data = pd.DataFrame(data['Data'])
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
        return self.data['volumefrom']

    # private methods

    def __prevalidate(self, interval: Interval, pair: SymbolPair, rows: int):
        # validate interval
        if interval is None:
            raise ValueError('Interval must be specified')
        if type(self).endpoints.get(interval) is None:
            raise ValueError('Interval must be daily, hourly or minute')
        # validate pair
        if pair is None:
            raise ValueError('Symbol pair must be specified')
        # validate rows
        if rows is None:
            raise ValueError('The number of rows must be specified')
