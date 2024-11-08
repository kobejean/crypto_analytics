import pytest

from crypto_analytics.types import Interval

# test unix

test_unix_data = [
    (Interval.SECOND, 1),
    (Interval.MINUTE, 60),
    (Interval.HOUR, 60*60),
    (Interval.DAY, 60*60*24),
]

def test_inteval_second_unix():
    # when
    unix_time = Interval.SECOND.unix
    # then
    expected = 1
    assert unix_time == expected

def test_inteval_minute_unix():
    # when
    unix_time = Interval.MINUTE.unix
    # then
    expected = 60
    assert unix_time == expected

def test_inteval_hour_unix():
    # when
    unix_time = Interval.HOUR.unix
    # then
    expected = 60*60
    assert unix_time == expected

def test_inteval_day_unix():
    # when
    unix_time = Interval.DAY.unix
    # then
    expected = 60*60*24
    assert unix_time == expected