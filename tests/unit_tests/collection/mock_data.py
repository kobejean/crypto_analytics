# crypto compare ohclv response data
cc_ohclv_success = {'Response': 'Success', 'Type': 100, 'Aggregated': False, 'Data': [{'time': 1560042540, 'close': 7906.14, 'high': 7906.45, 'low': 7903.86, 'open': 7903.86, 'volumefrom': 3.41, 'volumeto': 26958.13}, {'time': 1560042600, 'close': 7906.14, 'high': 7906.14, 'low': 7906.14, 'open': 7906.14, 'volumefrom': 0, 'volumeto': 0}], 'TimeTo': 1560042600, 'TimeFrom': 1560042540, 'FirstValueInArray': True, 'ConversionType': {'type': 'direct', 'conversionSymbol': ''}, 'RateLimit': {}, 'HasWarning': False}
cc_ohclv_null_param = {'Response': 'Error', 'Message': 'fsym param is empty or null.', 'HasWarning': False, 'Type': 2, 'RateLimit': {}, 'Data': {}, 'ParamWithError': 'fsym'}
# kraken ohclv response data
k_ohclv_success = {'error': [], 'result': {'XXBTZUSD': [[1560123060, '7633.2', '7636.2', '7633.2', '7635.6', '7635.7', '2.23099305', 6]], 'last': 1560123060}}
k_ohclv_incomplete_candle = {'error': [], 'result': {'XXBTZUSD': [[1560123060, '7633.2', '7636.2', '7633.2', '7635.6', '7635.7', '2.23099305', 6], [1560123120, '7635.6', '7635.6', '7630.5', '7633.1', '7630.6', '0.58258092', 2]], 'last': 1560123060}}
