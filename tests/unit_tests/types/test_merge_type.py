import pytest

from crypto_analytics.types import MergeType

# test to_merge_how

test_to_merge_how_data = [
    (MergeType.UNION, 'outer'),
    (MergeType.INTERSECT, 'inner'),
]


@pytest.mark.parametrize("merge_type,expected", test_to_merge_how_data)
def test_timedistance_v0(merge_type, expected):
    # when
    merge_how = merge_type.to_merge_how()
    # then
    assert merge_how == expected
