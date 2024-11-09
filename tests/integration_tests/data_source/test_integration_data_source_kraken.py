import pytest, requests, re, os
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from crypto_analytics.data_source import KrakenOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair, KrakenSymbolPairConverter
from crypto_analytics import utils


# mock data

k_ohclv_dtypes = {'time': np.int64, 'open': object, 'high': object, 'low': object, 'close': object, 'vwap': object, 'volume': object, 'count': np.int64 }
k_ohclv_columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
k_ohclv_past = [[1730764800, '67787.8', '70482.0', '67481.4', '69382.7', '69409.3', '2008.23627213', 30812], [1730851200, '69382.7', '76457.6', '69341.0', '75642.0', '73794.8', '8946.48732813', 69815]]
k_ohclv_past_df = pd.DataFrame(k_ohclv_past, columns=k_ohclv_columns).astype(k_ohclv_dtypes)

# fetch method tests

def test_kraken_ohlcv_fetch_past():
    # given
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    candles = KrakenOHLCV(Interval.DAY, pair, 2)
    candles.to_time = 1730937600.0
    # when
    data = candles.fetch()
    # then
    expected = k_ohclv_past_df
    # TODO: investigate why data is not consistent
    print(data)
    assert_frame_equal(data.astype(np.float32), expected.astype(np.float32), rtol=1e-6)

def test_kraken_ohlcv_fetch_live():
    # given
    interval = Interval.MINUTE
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    candles = KrakenOHLCV(interval, pair, 2)
    # when
    data = candles.fetch()
    # then
    expected = utils.time.candle_time(interval)
    assert data['time'][1] == expected
