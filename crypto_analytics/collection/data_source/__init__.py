from crypto_analytics.collection.data_source.base import DataSource
from crypto_analytics.collection.data_source.finance import FinancialDataSource

from crypto_analytics.collection.data_source.crypto_compare import CryptoCompare
from crypto_analytics.collection.data_source.coin_market_cap import CoinMarketCap
from crypto_analytics.collection.data_source.kraken import KrakenOHLC

__all__ = ["base", "crypto_compare", "coin_market_cap", "finance"]
