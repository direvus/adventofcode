from tests.common import get_day_result


YEAR = 2025


def test_y2025d01():
    assert get_day_result(YEAR, 1) == (3, 6)


def test_y2025d02():
    assert get_day_result(YEAR, 2) == (1227775554, 4174379265)


def test_y2025d03():
    assert get_day_result(YEAR, 3) == (357, 3121910778619)


def test_y2025d04():
    assert get_day_result(YEAR, 4) == (13, 43)


def test_y2025d05():
    assert get_day_result(YEAR, 5) == (3, 14)


def test_y2025d06():
    assert get_day_result(YEAR, 6) == (4277556, 3263827)


def test_y2025d07():
    assert get_day_result(YEAR, 7) == (21, 40)


def test_y2025d08():
    assert get_day_result(YEAR, 8) == (40, 25272)
