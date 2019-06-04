import pandas as pd
import json
import requests
from typing import Dict, Union

from enum import Enum
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from crypto_analytics.collection.data_source import DataSource
from crypto_analytics.types import Interval

class CoinMarketCap(DataSource):

    def __init__(self, key: str, endpoint: str):
        self.key = key
        self.endpoint = endpoint
        self.url = "https://pro-api.coinmarketcap.com/" + endpoint

        self.headers = {
            'X-CMC_PRO_API_KEY': key,
        }
        self.params: Dict[str, Union[int, str]] = {}

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
            self.data = pd.DataFrame(data['data'])
            return self.data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            self.data = pd.DataFrame()
            return self.data

    def write(self, filepath: str):
        self.data.to_csv(filepath)

    # TODO: needs implementation
    def get_time(self):
        return None
