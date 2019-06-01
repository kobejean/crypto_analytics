""" Contains data source classes """
from crypto_analytics.collection.data_source.base import DataSource
from crypto_analytics.collection.data_source.candles import CandlesDataSource

from crypto_analytics.collection.data_source.crypto_compare import CryptoCompareCandles
from crypto_analytics.collection.data_source.coin_market_cap import CoinMarketCap
from crypto_analytics.collection.data_source.kraken import KrakenCandles

__all__ = ["base", "candles", "crypto_compare", "coin_market_cap"]
