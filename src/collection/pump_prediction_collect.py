#!/usr/bin/env python
""" A script that collects data for pump prediction models """
from crypto_analytics.types import Interval
from crypto_analytics.collection.data_handler import PumpPredictionDataHandler
from crypto_analytics.types.symbol import Symbol, SymbolPair
from crypto_analytics.utils.time import get_latest_candle_time

# pair = input('Kraken pair code: ')
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# rows = int(input('Rows: '))
# output_file = input('CSV file path: ')

pair = SymbolPair(Symbol.USD, Symbol.BITCOIN)
rows = 120
output_file = 'pump_prediction_data.csv'

ppdh = PumpPredictionDataHandler(pair, rows)
ppdh.fetch()
print(ppdh.data)
ppdh.write(output_file)
