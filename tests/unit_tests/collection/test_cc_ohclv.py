import pandas as pd
import os
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval

from mock_data import cc_ohclv_success, cc_ohclv_null_param

def test_cc_ohlcv_fetch_success(requests_mock):
    # given
    mock_response = cc_ohclv_success
    endpoint = 'https://min-api.cryptocompare.com/data/histominute'
    requests_mock.get(endpoint, json=mock_response)
    candles = CryptoCompareOHLCV(Interval.MINUTE, 'BTC', 'USD', 1)
    # when
    data = candles.fetch()
    # then
    expected_data = pd.DataFrame(mock_response['Data'])
    assert_frame_equal(data, expected_data)

def test_cc_ohlcv_fetch_failure(requests_mock):
    # given
    mock_response = cc_ohclv_null_param
    endpoint = 'https://min-api.cryptocompare.com/data/histominute'
    requests_mock.get(endpoint, json=mock_response)
    candles = CryptoCompareOHLCV(Interval.MINUTE, None, 'USD', 1)
    # when
    data = candles.fetch()
    # then
    expected_data = pd.DataFrame(mock_response['Data'])
    assert_frame_equal(data, expected_data)
