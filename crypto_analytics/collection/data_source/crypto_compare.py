import pandas as pd
import json
import requests

from .finance import FinancialDataSource
from ...types import Interval

class CryptoCompare(DataSource):

    def __init__(self, endpoint: str, fsym: str, tsym: str, limit: int):
        self.endpoint = endpoint
        self.fsym = fsym
        self.tsym = tsym
        self.limit = limit
        self.valid_time_intervals = {
            Interval.MINUTE: 'data/histominute',
            Interval.HOURLY: 'data/histohour',
            Interval.DAILY: 'data/histoday',
        }
        super().__init__()

    def fetch(self) -> pd.DataFrame:
        url = 'https://min-api.cryptocompare.com/{}'.format(self.endpoint)

        parameters = {
            'fsym': self.fsym,
            'tsym': self.tsym,
            'limit': self.limit
        }
        response = requests.get(url, params=parameters)
        response.raise_for_status()

        data = response.json()
        self.data = pd.DataFrame(data['Data'])
        return self.data

    def write(self, filepath: str):
        self.data.to_csv (filepath)

    def get_time(self): 
        return self.data['time']

    def _get_ochlv(self, ochlv_type: str, interval: Interval):
        self.endpoint = self.valid_time_intervals.get(interval)
        if not self.endpoint:
            raise ValueError('Interval must be daily, hourly or minute')

        ochlv = self.fetch()
        return ochlv['Data'][ochlv_type]

    def get_open(self, interval: Interval):
        self._get_ochlv('open', interval)

    def get_close(self, interval: Interval):
        self._get_ochlv('close', interval)

    def get_high(self, interval: Interval):
        self._get_ochlv('high', interval)

    def get_low(self, interval: Interval):
        self._get_ochlv('low', interval)

    def get_volume(self, interval: Interval):
        self._get_ochlv('volume', interval)
