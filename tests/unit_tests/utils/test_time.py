import time

from crypto_analytics.types import Interval
from crypto_analytics.utils.time import get_latest_candle_time

def test_get_latest_candle_time(mocker):
    # given
    mocker.patch.object(time, 'time')
    time.time.return_value = 1562272820.272001
    interval = Interval.HOUR
    # when
    latest_candle_time = get_latest_candle_time(interval)
    # then
    expected = 1562266800
    assert latest_candle_time == expected
