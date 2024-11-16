from tests.common import get_day_result


YEAR = 2022


def test_y2022d01():
    assert get_day_result(YEAR, 1) == (24000, 45000)
