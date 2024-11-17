from tests.common import get_day_result


YEAR = 2022


def test_y2022d01():
    assert get_day_result(YEAR, 1) == (24000, 45000)


def test_y2022d02():
    assert get_day_result(YEAR, 2) == (15, 12)


def test_y2022d03():
    assert get_day_result(YEAR, 3) == (157, 70)
