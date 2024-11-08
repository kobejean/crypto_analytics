import pytest

from crypto_analytics.types import Interval

# test unix

test_unix_data = [
    (Interval.SECOND, 1),
    (Interval.MINUTE, 60),
    (Interval.HOUR, 60*60),
    (Interval.DAY, 60*60*24),
]
@pytest.mark.parametrize("interval,expected", test_unix_data)
def test_interval_unix(interval, expected):
    # when
    unix_time = interval.unix
    # then
    assert unix_time == expected

def test_inteval_second_unix():
    # when
    unix_time = Interval.SECOND.unix
    # then
    expected = 1
    assert unix_time == expected