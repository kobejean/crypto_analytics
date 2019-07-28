import pytest, time
import pandas as pd
from pandas.util.testing import assert_frame_equal

from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair, CryptoCompareSymbolPairConverter, CryptoCompareSymbolPair

# mock data

cc_ohclv_success = {'Response': 'Success', 'Type': 100, 'Aggregated': False, 'Data': [{'time': 1560042540, 'close': 7906.14, 'high': 7906.45, 'low': 7903.86, 'open': 7903.86, 'volumefrom': 3.41, 'volumeto': 26958.13}, {'time': 1560042600, 'close': 7906.14, 'high': 7906.14, 'low': 7906.14, 'open': 7906.14, 'volumefrom': 0, 'volumeto': 0}], 'TimeTo': 1560042600, 'TimeFrom': 1560042540, 'FirstValueInArray': True, 'ConversionType': {'type': 'direct', 'conversionSymbol': ''}, 'RateLimit': {}, 'HasWarning': False}
cc_ohclv_success_df = pd.DataFrame([cc_ohclv_success['Data'][0]])
# cc_ohclv_null_param = {'Response': 'Error', 'Message': 'fsym param is empty or null.', 'HasWarning': False, 'Type': 2, 'RateLimit': {}, 'Data': {}, 'ParamWithError': 'fsym'}


# fixtures

@pytest.fixture(scope='function')
def mock_fetch(requests_mock, mocker):
    def setup_fn(sympair, candle_time, requests_mock_params):
        # mock symbol pair conversion
        mocker.patch.object(CryptoCompareSymbolPairConverter, 'from_pair')
        CryptoCompareSymbolPairConverter.from_pair.return_value = sympair
        # mock time function
        mocker.patch.object(time, 'time')
        time.time.return_value = candle_time
        # mock endpoint response
        endpoint = 'https://min-api.cryptocompare.com/data/histominute'
        requests_mock.get(endpoint, **requests_mock_params)

    return setup_fn


# fetch method tests

def test_crypto_compare_ohlcv_fetch_success(mock_fetch):
    # get
    mock_sympair = CryptoCompareSymbolPair('BTC', 'USD')
    candle_time = 1560042663.56
    mock_fetch(mock_sympair, candle_time, { 'json' : cc_ohclv_success })
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    candles = CryptoCompareOHLCV(Interval.MINUTE, pair, 1)
    # when
    data = candles.fetch()
    # then
    expected_data = cc_ohclv_success_df
    assert_frame_equal(data, expected_data)
