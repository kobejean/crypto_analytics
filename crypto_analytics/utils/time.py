import time

from crypto_analytics.types import Interval

def get_latest_candle_time(interval: Interval) -> int:
    interval_duration = interval.to_unix_time()
    now = time.time()
    candel_close_time = int((now // interval_duration) * interval_duration)
    candel_open_time = candel_close_time - interval_duration
    return candel_open_time
