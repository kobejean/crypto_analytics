import requests, time, math
import pandas as pd
from typing import Dict, Union, Optional, cast

from crypto_analytics.collection.data_source import OHLCVDataSource
from crypto_analytics.types  import Interval
from crypto_analytics.types.symbol import SymbolPair, CryptoCompareSymbolPairConverter
from crypto_analytics import utils

class CryptoCompareOHLCV(OHLCVDataSource):
    max_rows = 2000
    endpoints = {
        Interval.MINUTE: 'data/histominute',
        Interval.HOUR: 'data/histohour',
        Interval.DAY: 'data/histoday',
    }

    def fetch(self) -> pd.DataFrame:
        self.prevalidate()
        
        endpoint = type(self).endpoints.get(self.interval)
        url = 'https://min-api.cryptocompare.com/{}'.format(endpoint)

        converted_pair = CryptoCompareSymbolPairConverter.from_pair(self.pair)
        toTs = math.floor(self.to_time)

        parameters: Dict[str, Union[int, str]] = {
            'fsym': converted_pair.fsym,
            'tsym': converted_pair.tsym,
            'limit': self.rows,
            'toTs': toTs,
        }
        response = requests.get(url, params=parameters)
        response.raise_for_status()

        data = response.json()
        self._data = pd.DataFrame(data['Data']).head(self.rows)

        self.validate()
        return self.data

    @property
    def time(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['time']

    @property
    def open(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['open']

    @property
    def close(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['close']

    @property
    def high(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['high']

    @property
    def low(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['low']

    @property
    def volume(self) -> pd.Series:
        return cast(pd.DataFrame, self.data)['volumefrom']
