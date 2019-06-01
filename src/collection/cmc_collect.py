#!/usr/bin/env python
import json

import crypto_analytics
from crypto_analytics.collection.data_source import CoinMarketCap

params = input('Parameters: ')
params = json.loads(params)
endpoint = input('Endpoint: ')
key = input('Key: ')
output_file = input('Output File: ')

coin_market_cap = CoinMarketCap(key, endpoint)
coin_market_cap.fetch()
coin_market_cap.write(output_file)
