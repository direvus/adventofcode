from tests.common import get_day_result


YEAR = 2020


def test_y2020d01():
    assert get_day_result(YEAR, 1) == (514579, 241861950)


def test_y2020d02():
    assert get_day_result(YEAR, 2) == (2, 1)


def test_y2020d03():
    assert get_day_result(YEAR, 3) == (7, 336)


def test_y2020d04():
    assert get_day_result(YEAR, 4) == (2, 2)


def test_y2020d05():
    from y2020.d05 import get_seat

    assert get_seat('FBFBBFFRLR') == (44, 5)
    assert get_day_result(YEAR, 5) == (820, None)


def test_y2020d06():
    assert get_day_result(YEAR, 6) == (11, 6)
