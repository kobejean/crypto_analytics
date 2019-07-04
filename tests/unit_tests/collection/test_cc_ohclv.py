import pandas as pd
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair

from mock_data import cc_ohclv_success

def test_cc_ohlcv_fetch_success(requests_mock):
    # given
    mock_response = cc_ohclv_success
    endpoint = 'https://min-api.cryptocompare.com/data/histominute'
    requests_mock.get(endpoint, json=mock_response)
    pair = SymbolPair(Symbol.USD, Symbol.BITCOIN)
    candles = CryptoCompareOHLCV(Interval.MINUTE, pair, 1)
    # when
    data = candles.fetch()
    # then
    expected_data = pd.DataFrame(mock_response['Data'])
    assert_frame_equal(data, expected_data)
