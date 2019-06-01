#!/usr/bin/env python
from __context__ import crypto_analytics
from crypto_analytics.collection.data_source import CryptoCompareCandles
from crypto_analytics.types import Interval

# interval = Interval(input('Interval: '))
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# limit = input('Limit: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
fsym = 'BTC'
tsym = 'USD'
limit = 59
output_file = 'cc_collect_data.csv'

candles = CryptoCompareCandles(interval, fsym, tsym, limit)
candles.fetch()
print(candles.data)
print('time:', candles.get_time().head(), sep='\n')
print('open:', candles.get_open().head(), sep='\n')
print('high:', candles.get_high().head(), sep='\n')
print('low:', candles.get_low().head(), sep='\n')
print('close:', candles.get_close().head(), sep='\n')
print('volume:', candles.get_volume().head(), sep='\n')
candles.write(output_file)
