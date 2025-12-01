from tests.common import get_day_result


YEAR = 2025


def test_y2025d01():
    assert get_day_result(YEAR, 1) == (3, 6)
