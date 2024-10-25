from tests.common import get_day_result


YEAR = 2021


def test_y2021d01():
    assert get_day_result(YEAR, 1) == (7, 5)


def test_y2021d02():
    assert get_day_result(YEAR, 2) == (150, 900)
