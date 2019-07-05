import time

from crypto_analytics.types import Interval
from crypto_analytics import utils

def test_candle_time(mocker):
    # given
    mocker.patch.object(time, 'time')
    time.time.return_value = 1562272820.272001
    interval = Interval.HOUR
    # when
    candle_time = utils.time.candle_time(interval)
    # then
    expected = 1562266800
    assert candle_time == expected
