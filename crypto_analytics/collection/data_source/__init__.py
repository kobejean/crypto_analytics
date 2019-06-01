""" Contains data source classes """
from .base import DataSource
from .candles import CandlesDataSource
from .crypto_compare import CryptoCompareCandles
from .coin_market_cap import CoinMarketCap
from .kraken import KrakenCandles

__all__ = ["base", "candles", "crypto_compare", "coin_market_cap"]
