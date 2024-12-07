from tests.common import get_day_result


YEAR = 2024


def test_y2024d01():
    assert get_day_result(YEAR, 1) == (11, 31)


def test_y2024d02():
    assert get_day_result(YEAR, 2) == (2, 4)


def test_y2024d03():
    assert get_day_result(YEAR, 3) == (161, 48)


def test_y2024d04():
    assert get_day_result(YEAR, 4) == (18, 9)


def test_y2024d05():
    assert get_day_result(YEAR, 5) == (143, 123)


def test_y2024d06():
    assert get_day_result(YEAR, 6) == (41, 6)


def test_y2024d07():
    assert get_day_result(YEAR, 7) == (3749, 11387)
