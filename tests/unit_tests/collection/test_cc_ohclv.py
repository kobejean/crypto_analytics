import json
import pandas as pd
import os
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval

def _get_json(relpath):
    dir = os.path.dirname(__file__)
    filepath = os.path.join(dir, relpath)
    with open(filepath) as file:
        return json.load(file)

def test_cc_ohlcv_fetch_success(requests_mock):
    mock_response = _get_json('mock_data/cc_ohclv_success.json')
    expected_data = pd.DataFrame(mock_response['Data'])
    endpoint = 'https://min-api.cryptocompare.com/data/histominute'
    requests_mock.get(endpoint, json=mock_response)
    candles = CryptoCompareOHLCV(Interval.MINUTE, 'BTC', 'USD', 1)

    data = candles.fetch()

    assert_frame_equal(data, expected_data)
