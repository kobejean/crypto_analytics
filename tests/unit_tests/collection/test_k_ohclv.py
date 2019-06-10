import pytest
import requests
import pandas as pd
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import KrakenOHLCV
from crypto_analytics.types import Interval

from mock_data import k_ohclv_success, k_ohclv_incomplete_candle

# fetch method tests

def test_k_ohlcv_fetch_success(requests_mock):
    # given
    mock_response = k_ohclv_success
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, json=mock_response)
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    # when
    data = candles.fetch()
    # then
    columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    expected_data = pd.DataFrame(mock_response['result']['XXBTZUSD'], columns=columns)
    assert_frame_equal(data, expected_data)

def test_k_ohlcv_fetch_not_enough_rows(requests_mock):
    # given
    mock_response = k_ohclv_success
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, json=mock_response)
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 2, 1560123060)
    # when
    with pytest.raises(ValueError, match=r'row'):
        data = candles.fetch()
    # then
    assert candles.data == None

def test_k_ohlcv_fetch_incomplete_candle(requests_mock):
    # given
    mock_response = k_ohclv_incomplete_candle
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, json=mock_response)
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 2, 1560123060)
    # when
    with pytest.raises(ValueError, match=r'candle'):
        data = candles.fetch()
    # then
    assert candles.data == None

def test_k_ohlcv_fetch_connect_timeout(requests_mock):
    # given
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, exc=requests.exceptions.ConnectTimeout)
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    # when
    with pytest.raises(requests.exceptions.ConnectTimeout):
        data = candles.fetch()
    # then
    assert candles.data == None
