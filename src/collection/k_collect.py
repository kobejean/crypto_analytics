#!/usr/bin/env python
from crypto_analytics.collection.data_source import KrakenOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair

# interval = Interval(input('Interval: '))
# pair = input('Pair: ')
# rows = input('Rows: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
pair = SymbolPair(Symbol.USD, Symbol.BITCOIN)
rows = 5
output_file = 'k_collect_data.csv'

candles = KrakenOHLCV(interval, pair, rows)
candles.fetch()
print(candles.data)
print('time:', candles.get_time().head(), sep='\n')
print('open:', candles.get_open().head(), sep='\n')
print('high:', candles.get_high().head(), sep='\n')
print('low:', candles.get_low().head(), sep='\n')
print('close:', candles.get_close().head(), sep='\n')
print('volume:', candles.get_volume().head(), sep='\n')
candles.write(output_file)
