from tests.common import get_day_result


YEAR = 2020


def test_y2020d01():
    assert get_day_result(YEAR, 1) == (514579, 241861950)


def test_y2020d02():
    assert get_day_result(YEAR, 2) == (2, 1)


def test_y2020d03():
    assert get_day_result(YEAR, 3) == (7, 336)
