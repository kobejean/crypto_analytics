#!/usr/bin/env python
import time

import crypto_analytics
from crypto_analytics.collection.data_source import KrakenOHLCV
from crypto_analytics.types import Interval

# interval = Interval(input('Interval: '))
# pair = input('Pair: ')
# since = input('Since: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
pair = 'XXBTZUSD'
interval_duration = interval.to_unix_time()
# calculate time at 60 intervals ago
since = int(time.time() - 60*interval_duration)
output_file = 'k_collect_data.csv'

candles = KrakenOHLCV(interval, pair, since)
candles.fetch()
print(candles.data)
print('time:', candles.get_time().head(), sep='\n')
print('open:', candles.get_open().head(), sep='\n')
print('high:', candles.get_high().head(), sep='\n')
print('low:', candles.get_low().head(), sep='\n')
print('close:', candles.get_close().head(), sep='\n')
print('volume:', candles.get_volume().head(), sep='\n')
candles.write(output_file)
