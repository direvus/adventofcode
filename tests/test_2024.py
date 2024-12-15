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


def test_y2024d08():
    assert get_day_result(YEAR, 8) == (14, 34)


def test_y2024d09():
    assert get_day_result(YEAR, 9) == (1928, 2858)


def test_y2024d10():
    assert get_day_result(YEAR, 10) == (36, 81)


def test_y2024d11():
    assert get_day_result(YEAR, 11) == (55312, 65601038650482)


def test_y2024d12():
    assert get_day_result(YEAR, 12) == (1930, 1206)


def test_y2024d13():
    assert get_day_result(YEAR, 13) == (480, 875318608908)


def test_y2024d14():
    assert get_day_result(YEAR, 14) == (12, 0)


def test_y2024d15():
    assert get_day_result(YEAR, 15) == (10092, 9021)
