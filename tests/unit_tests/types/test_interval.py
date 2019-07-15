import pytest

from crypto_analytics.types import Interval

# test to_unix_time

test_to_unix_time_data = [
    (Interval.MINUTE, 60),
    (Interval.HOUR, 60*60),
    (Interval.DAY, 60*60*24),
]
@pytest.mark.parametrize("interval,expected", test_to_unix_time_data)
def test_interval_to_unix_time(interval, expected):
    # when
    unix_time = interval.to_unix_time()
    # then
    assert unix_time == expected
