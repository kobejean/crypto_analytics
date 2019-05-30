import pandas as pd
import json
import requests

from enum import Enum
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from .base import DataSource
from ...types.interval import Interval

class CoinMarketCap(DataSource):

    def __init__(self, key: str, endpoint: str):
        self.key = key
        self.endpoint = endpoint
        self.url = "https://pro-api.coinmarketcap.com/" + endpoint

        self.headers = {
            'X-CMC_PRO_API_KEY': key,
        }
        self.params = {}

        self.session = Session() 
        self.session.headers.update(self.headers)        

        super().__init__()

    def fetch(self) -> pd.DataFrame:
        try:
            response = self.session.get(self.url, params=self.params)
            response.raise_for_status
            if response.status_code != 200:
                raise ConnectionError('Code: {}\nReason: {}'.format(response.status_code,
                                                                    response.reason))

            data = response.json()
            self.df = pd.DataFrame(data['data'])
            return self.df
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            self.df = pd.DataFrame()
            return self.df

    def write(self, filepath: str):
        self.df.to_csv(filepath)
