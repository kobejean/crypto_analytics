import pytest, time, heapq
import pandas as pd
import math
from unittest.mock import call

from crypto_analytics.controller import ClosePriceController
from crypto_analytics.data_source import StableWorldOHLCV
from crypto_analytics.types import Interval
from crypto_analytics.types.symbol import Symbol, SymbolPair
from crypto_analytics import utils

# run method tests

def test_close_price_controller_run_usdjpy():
    # given
    interval = Interval.MINUTE
    pair = SymbolPair(Symbol.USD, Symbol.JPY)
    datasource = StableWorldOHLCV(interval, pair, 10)
    controller = ClosePriceController(datasource)
    # when
    close_price = controller.run()
    # then
    expected = 152.49 # usdjpy
    assert math.isclose(close_price, expected, abs_tol=1e-2)


def test_close_price_controller_run_jpyvnd():
    # given
    interval = Interval.MINUTE
    pair = SymbolPair(Symbol.JPY, Symbol.VND)
    rows = 10
    datasource = StableWorldOHLCV(interval, pair, rows)
    controller = ClosePriceController(datasource)
    # when
    close_price = controller.run()
    # then
    expected = 165.75 # jpyvnd
    assert math.isclose(close_price, expected, abs_tol=1e-2)

