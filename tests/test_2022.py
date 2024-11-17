from tests.common import get_day_result


YEAR = 2022


def test_y2022d01():
    assert get_day_result(YEAR, 1) == (24000, 45000)


def test_y2022d02():
    assert get_day_result(YEAR, 2) == (15, 12)


def test_y2022d03():
    assert get_day_result(YEAR, 3) == (157, 70)


def test_y2022d04():
    assert get_day_result(YEAR, 4) == (2, 4)


def test_y2022d05():
    assert get_day_result(YEAR, 5) == ('CMZ', 'MCD')


def test_y2022d06():
    assert get_day_result(YEAR, 6) == (7, 19)
