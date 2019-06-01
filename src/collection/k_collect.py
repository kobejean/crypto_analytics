#!/usr/bin/env python
import time

import crypto_analytics
from crypto_analytics.collection.data_source import KrakenOHLC
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

kraken_ohlc = KrakenOHLC(interval, pair, since)
kraken_ohlc.fetch()
print(kraken_ohlc.data)
kraken_ohlc.write(output_file)
