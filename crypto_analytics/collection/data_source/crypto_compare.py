import pandas as pd
import json
import requests

from .base import DataSource
from ...types.interval import Interval

class CryptoCompare(DataSource):

    def __init__(self, interval: Interval, fsym: str, tsym: str, limit: int):
        self.interval = interval
        self.fsym = fsym
        self.tsym = tsym
        self.limit = limit
        super().__init__()

    def fetch(self) -> pd.DataFrame:
        paths = {
            Interval.MINUTE: 'data/histominute',
            Interval.HOURLY: 'data/histohour',
            Interval.DAILY: 'data/histoday',
        }
        path = paths.get(self.interval)
        if not path:
            raise ValueError('Interval must be daily, hourly or minute')

        url = 'https://min-api.cryptocompare.com/{}'.format(path)

        parameters = {
            'fsym': self.fsym,
            'tsym': self.tsym,
            'limit': self.limit
        }
        response = requests.get(url, params=parameters)
        response.raise_for_status()

        data = response.json()
        self.df = pd.DataFrame(data['Data'])
        return self.df


    def write(self, filepath: str):
        self.df.to_csv(filepath)
