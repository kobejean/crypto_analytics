#!/usr/bin/env python
""" A script that collects data for pump prediction models """
import crypto_analytics
from crypto_analytics.collection.data_handler import PumpPredictionDataHandler

# pair = input('Kraken pair code: ')
# fsym = input('Symbols: ')
# tsym = input('Convert Symbols: ')
# rows = int(input('Rows: '))
# output_file = input('CSV file path: ')

pair = 'XXBTZUSD'
fsym = 'BTC'
tsym = 'USD'
rows = 120
output_file = 'pump_prediction_data.csv'

ppdh = PumpPredictionDataHandler(pair, fsym, tsym, rows)
ppdh.fetch()
print(ppdh.data)
ppdh.write(output_file)
