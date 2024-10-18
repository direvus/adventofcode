from tests.common import get_day_result


YEAR = 2020


def test_y2020d01():
    assert get_day_result(YEAR, 1) == (0, 0)
