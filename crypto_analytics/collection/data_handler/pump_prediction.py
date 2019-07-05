import time
from typing import Optional

from crypto_analytics.collection.data_handler import ColumnMapper
from crypto_analytics.collection.data_source import CryptoCompareOHLCV, KrakenOHLCV
from crypto_analytics.types import Interval, MergeType
from crypto_analytics.types.symbol import SymbolPair
from crypto_analytics.utils.typing import RealNumber
from crypto_analytics import utils

class PumpPredictionDataHandler(ColumnMapper):
    """ A data handler used to transdorm data for pump prediction models """

    def __init__(self, pair: SymbolPair, rows: int, to_time: Optional[RealNumber] = None):
        """ Creates the PumpPredictionDataHandler data handler object """
        interval = Interval.MINUTE
        merge_type = MergeType.INTERSECT
        last_time = utils.time.candle_time(interval, to_time)

        data_sources = {
            'crypto_compare_ohlcv': CryptoCompareOHLCV(interval, pair, rows, last_time),
            'kraken_ohlcv': KrakenOHLCV(interval, pair, rows, last_time),
        }
        column_map = {
            'crypto_compare_ohlcv': {
                'time': 'time',
                'open': 'cc_open',
                'high': 'cc_high',
                'low': 'cc_low',
                'close': 'cc_close',
                'volumefrom': 'cc_volumefrom',
                'volumeto': 'cc_volumeto',
            },
            'kraken_ohlcv': {
                'time': 'time',
                'open': 'k_open',
                'high': 'k_high',
                'low': 'k_low',
                'close': 'k_close',
                'vwap': 'k_vwap',
                'volume': 'k_volume',
                'count': 'k_count',
            },
        }
        super().__init__(data_sources, column_map, merge_type)
