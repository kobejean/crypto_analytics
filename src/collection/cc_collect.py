#!/usr/bin/env python
from __context__ import stock_analytics
from stock_analytics.collection.data_source import CryptoCompare
from stock_analytics.types import Interval

interval = Interval(input('Interval: '))
fsym = input('Symbols: ')
tsym = input('Convert Symbols: ')
limit = input('Limit: ')

crypto_compare = CryptoCompare(interval, fsym, tsym, limit)
crypto_compare.fetch()
print(crypto_compare.df)
crypto_compare.write(input('CSV file path: '))
