#!/usr/bin/env python
from crypto_analytics.collection.data_source import CryptoCompareOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair
from crypto_analytics.utils.time import get_latest_candle_time

# interval = Interval(input('Interval: '))
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# limit = input('Limit: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
rows = 60
last_time = get_latest_candle_time(interval)
output_file = 'cc_collect_data.csv'

candles = CryptoCompareOHLCV(interval, pair, rows, last_time)
candles.fetch()
print(candles.data)
print('time:', candles.get_time().head(), sep='\n')
print('open:', candles.get_open().head(), sep='\n')
print('high:', candles.get_high().head(), sep='\n')
print('low:', candles.get_low().head(), sep='\n')
print('close:', candles.get_close().head(), sep='\n')
print('volume:', candles.get_volume().head(), sep='\n')
candles.write(output_file)
