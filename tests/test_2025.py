from tests.common import get_day_result


YEAR = 2025


def test_y2025d01():
    assert get_day_result(YEAR, 1) == (3, 6)


def test_y2025d02():
    assert get_day_result(YEAR, 2) == (1227775554, 4174379265)


def test_y2025d03():
    assert get_day_result(YEAR, 3) == (357, 0)
