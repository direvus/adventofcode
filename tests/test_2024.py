from tests.common import get_day_result


YEAR = 2024


def test_y2024d01():
    assert get_day_result(YEAR, 1) == (11, 31)


def test_y2024d02():
    assert get_day_result(YEAR, 2) == (2, 4)
