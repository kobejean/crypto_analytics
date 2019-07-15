import time
from typing import Optional

from crypto_analytics.types import Interval
from crypto_analytics.utils.typing import RealNumber, unwrap, coalesce

def candle_time(interval: Interval, timestamp: Optional[RealNumber] = None) -> int:
    """
    Returns the last completed candle time before a given timestamp
    if no timestamp is provided it will use the current time
    """
    interval_duration = interval.to_unix_time()
    unwrapped_time = coalesce(timestamp, lambda: time.time())
    candel_close_time = int(unwrapped_time // interval_duration) * interval_duration
    candel_open_time = candel_close_time - interval_duration
    return candel_open_time
