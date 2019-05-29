#!/usr/bin/env python
from __context__ import crypto_analytics
from crypto_analytics.collection.data_source import CryptoCompare
from crypto_analytics.types import Interval

interval = Interval(input('Interval: '))
fsym = input('Symbols: ')
tsym = input('Convert Symbols: ')
limit = input('Limit: ')

crypto_compare = CryptoCompare(interval, fsym, tsym, limit)
crypto_compare.fetch()
print(crypto_compare.df)
crypto_compare.write(input('CSV file path: '))
