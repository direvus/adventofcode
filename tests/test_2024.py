from tests.common import get_day_result


YEAR = 2024


def test_y2024d01():
    assert get_day_result(YEAR, 1) == (11, 31)


def test_y2024d02():
    assert get_day_result(YEAR, 2) == (2, 4)


def test_y2024d03():
    assert get_day_result(YEAR, 3) == (161, 48)


def test_y2024d04():
    assert get_day_result(YEAR, 4) == (18, 0)
