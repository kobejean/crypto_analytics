import time

from crypto_analytics.types import Interval

def get_latest_candle_time(interval: Interval) -> int:
    interval_duration = interval.to_unix_time()
    now = time.time()
    latest_time = (now//interval_duration - 1) * interval_duration
    return int(latest_time)
