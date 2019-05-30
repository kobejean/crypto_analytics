#!/usr/bin/env python
from __context__ import crypto_analytics
from crypto_analytics.collection.data_source import CryptoCompare
from crypto_analytics.types import Interval

# interval = Interval(input('Interval: '))
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# limit = input('Limit: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
fsym = 'BTC'
tsym = 'USD'
limit = 99
output_file = 'cc_collect_data.csv'

crypto_compare = CryptoCompare(interval, fsym, tsym, limit)
crypto_compare.fetch()
print(crypto_compare.data)
crypto_compare.write(output_file)
