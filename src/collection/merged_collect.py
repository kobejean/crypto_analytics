#!/usr/bin/env python
import time

from __context__ import crypto_analytics
from crypto_analytics.collection.data_source import KrakenOHLC, CryptoCompare
from crypto_analytics.collection.data_handler import ColumnMapper
from crypto_analytics.types import Interval, MergeType

# interval = Interval(input('Interval: '))
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# limit = input('Limit: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
merge_type = MergeType.INTERSECT
pair = 'XXBTZUSD'
fsym = 'BTC'
tsym = 'USD'
limit = 59
row_count = limit + 1
interval_duration = interval.to_unix_time()
# calculate time at row_count intervals ago
since = int(time.time() - row_count*interval_duration)

output_file = 'merged_collect_data.csv'

data_sources = {
    'crypto_compare': CryptoCompare(interval, fsym, tsym, limit),
    'kraken_ohlc': KrakenOHLC(interval, pair, since),
}

column_map = {
    'crypto_compare': {
        'time': 'time',
        'open': 'cc_open',
        'high': 'cc_high',
        'low': 'cc_low',
        'close': 'cc_close',
        'volumefrom': 'cc_volumefrom',
        'volumeto': 'cc_volumeto',
    },
    'kraken_ohlc': {
        'time': 'time',
        'open': 'k_open',
        'high': 'k_high',
        'low': 'k_low',
        'close': 'k_close',
        'vwap': 'k_vwap',
        'volume': 'k_volume',
    },
}

column_mapper = ColumnMapper(data_sources, column_map, merge_type)
column_mapper.fetch()
print(column_mapper.data)
column_mapper.write(output_file)
