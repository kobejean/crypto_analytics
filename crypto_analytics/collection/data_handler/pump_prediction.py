import time

from .column_mapper import ColumnMapper
from ..data_source import DataSource, CryptoCompareCandles, KrakenCandles
from ...types import Interval, MergeType

class PumpPredictionDataHandler(ColumnMapper):
    """ A data handler used to transdorm data for pump prediction models """

    def __init__(self, pair: str, fsym: str, tsym: str, rows: int):
        """ Creates the PumpPredictionDataHandler data handler object """
        interval = Interval.MINUTE
        merge_type = MergeType.INTERSECT
        limit = rows - 1
        interval_duration = interval.to_unix_time()
        # calculate time at rows intervals ago
        since = int(time.time() - rows*interval_duration)

        data_sources = {
            'crypto_compare_candles': CryptoCompareCandles(interval, fsym, tsym, limit),
            'kraken_candles': KrakenCandles(interval, pair, since),
        }
        column_map = {
            'crypto_compare_candles': {
                'time': 'time',
                'open': 'cc_open',
                'high': 'cc_high',
                'low': 'cc_low',
                'close': 'cc_close',
                'volumefrom': 'cc_volumefrom',
                'volumeto': 'cc_volumeto',
            },
            'kraken_candles': {
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
