#!/usr/bin/env python
from crypto_analytics.data_source import StableWorldOHLCV
from crypto_analytics.controller import ClosePriceController
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair

# interval = Interval(input('Interval: '))
# pair = input('Pair: ')
# rows = input('Rows: ')
# output_file = input('CSV file path: ')

interval = Interval.MINUTE
pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
rows = 5
output_file = 'stable_collect_data.csv'

candles = StableWorldOHLCV(interval, pair, rows)
candles.fetch()
print(candles.data)
print('time:', candles.time.head(), sep='\n')
print('open:', candles.open.head(), sep='\n')
print('high:', candles.high.head(), sep='\n')
print('low:', candles.low.head(), sep='\n')
print('close:', candles.close.head(), sep='\n')
print('volume:', candles.volume.head(), sep='\n')
candles.write(output_file)

pair = SymbolPair(Symbol.USD, Symbol.JPY)
candles = StableWorldOHLCV(interval, pair, 1)
candles.fetch()
cp_controller = ClosePriceController(candles)
todays_price = cp_controller.run()
print(f'{todays_price=}')
