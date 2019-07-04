import pandas as pd
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair

# mock data

cc_ohclv_success = {'Response': 'Success', 'Type': 100, 'Aggregated': False, 'Data': [{'time': 1560042540, 'close': 7906.14, 'high': 7906.45, 'low': 7903.86, 'open': 7903.86, 'volumefrom': 3.41, 'volumeto': 26958.13}, {'time': 1560042600, 'close': 7906.14, 'high': 7906.14, 'low': 7906.14, 'open': 7906.14, 'volumefrom': 0, 'volumeto': 0}], 'TimeTo': 1560042600, 'TimeFrom': 1560042540, 'FirstValueInArray': True, 'ConversionType': {'type': 'direct', 'conversionSymbol': ''}, 'RateLimit': {}, 'HasWarning': False}
cc_ohclv_null_param = {'Response': 'Error', 'Message': 'fsym param is empty or null.', 'HasWarning': False, 'Type': 2, 'RateLimit': {}, 'Data': {}, 'ParamWithError': 'fsym'}


def test_cc_ohlcv_fetch_success(requests_mock):
    # given
    mock_response = cc_ohclv_success
    endpoint = 'https://min-api.cryptocompare.com/data/histominute'
    requests_mock.get(endpoint, json=mock_response)
    pair = SymbolPair(Symbol.USD, Symbol.BITCOIN)
    candles = CryptoCompareOHLCV(Interval.MINUTE, pair, 1, 1560042600)
    # when
    data = candles.fetch()
    # then
    expected_data = pd.DataFrame(mock_response['Data'])
    assert_frame_equal(data, expected_data)
