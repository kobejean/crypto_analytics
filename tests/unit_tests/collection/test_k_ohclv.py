import pytest, requests, re, os
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal, assert_series_equal

from crypto_analytics.collection.data_source import KrakenOHLCV
from crypto_analytics.types import Interval

# mock data

k_ohclv_dtypes = {'time': np.int64, 'open': object, 'high': object, 'low': object, 'close': object, 'vwap': object, 'volume': object, 'count': np.int64 }
k_ohclv_columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
k_ohclv_success = {'error': [], 'result': {'XXBTZUSD': [[1560123060, '7633.2', '7636.2', '7633.2', '7635.6', '7635.7', '2.23099305', 6]], 'last': 1560123060}}
k_ohclv_success_df = pd.DataFrame(k_ohclv_success['result']['XXBTZUSD'], columns=k_ohclv_columns).astype(k_ohclv_dtypes)
k_ohclv_incomplete_candle = {'error': [], 'result': {'XXBTZUSD': [[1560123060, '7633.2', '7636.2', '7633.2', '7635.6', '7635.7', '2.23099305', 6], [1560123120, '7635.6', '7635.6', '7630.5', '7633.1', '7630.6', '0.58258092', 2]], 'last': 1560123060}}
k_ohclv_incomplete_candle_df = pd.DataFrame(k_ohclv_incomplete_candle['result']['XXBTZUSD'], columns=k_ohclv_columns).astype(k_ohclv_dtypes)

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
    expected_data = k_ohclv_success_df
    assert_frame_equal(data, expected_data)

def test_k_ohlcv_fetch_not_enough_rows(requests_mock):
    # given
    mock_response = k_ohclv_success
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, json=mock_response)
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 2, 1560123060)
    # when
    error_msg_regx = re.compile('row', re.IGNORECASE)
    with pytest.raises(ValueError, match=error_msg_regx):
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
    error_msg_regx = re.compile('candle', re.IGNORECASE)
    with pytest.raises(ValueError, match=error_msg_regx):
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

def test_k_ohlcv_fetch_invalid_interval(requests_mock):
    # given
    mock_response = k_ohclv_success
    endpoint = 'https://api.kraken.com/0/public/OHLC'
    requests_mock.get(endpoint, json=mock_response)
    candles = KrakenOHLCV('', 'XXBTZUSD', 1, 1560123060)
    # when
    error_msg_regx = re.compile('interval', re.IGNORECASE)
    with pytest.raises(ValueError, match=error_msg_regx):
        data = candles.fetch()
    # then
    assert candles.data == None

# get * method tests

def test_k_ohlcv_get_time(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_time()
    # then
    expected_data = k_ohclv_success_df['time']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_open(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_open()
    # then
    expected_data = k_ohclv_success_df['open']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_open(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_open()
    # then
    expected_data = k_ohclv_success_df['open']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_high(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_high()
    # then
    expected_data = k_ohclv_success_df['high']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_low(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_low()
    # then
    expected_data = k_ohclv_success_df['low']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_close(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_close()
    # then
    expected_data = k_ohclv_success_df['close']
    assert_series_equal(data, expected_data)

def test_k_ohlcv_get_volume(requests_mock):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    # when
    data = candles.get_volume()
    # then
    expected_data = k_ohclv_success_df['volume']
    assert_series_equal(data, expected_data)

# write method tests

def test_k_ohlcv_write(requests_mock, tmp_dir):
    # given
    candles = KrakenOHLCV(Interval.MINUTE, 'XXBTZUSD', 1, 1560123060)
    candles.data = k_ohclv_success_df
    filepath = os.path.join(tmp_dir, 'test_k_ohlcv_write.csv')
    # when
    candles.write(filepath)
    # then
    data = pd.read_csv(filepath, dtype=k_ohclv_dtypes)
    expected_data = k_ohclv_success_df
    assert_frame_equal(data, expected_data)
