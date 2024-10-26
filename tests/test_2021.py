from tests.common import get_day_result


YEAR = 2021


def test_y2021d01():
    assert get_day_result(YEAR, 1) == (7, 5)


def test_y2021d02():
    assert get_day_result(YEAR, 2) == (150, 900)


def test_y2021d03():
    assert get_day_result(YEAR, 3) == (198, 230)


def test_y2021d04():
    assert get_day_result(YEAR, 4) == (4512, 1924)


def test_y2021d05():
    assert get_day_result(YEAR, 5) == (5, 12)


def test_y2021d06():
    assert get_day_result(YEAR, 6) == (5934, 26984457539)


def test_y2021d07():
    assert get_day_result(YEAR, 7) == (37, 168)


def test_y2021d08():
    assert get_day_result(YEAR, 8) == (26, 61229)


def test_y2021d09():
    assert get_day_result(YEAR, 9) == (15, 1134)


def test_y2021d10():
    assert get_day_result(YEAR, 10) == (26397, 288957)


def test_y2021d11():
    assert get_day_result(YEAR, 11) == (1656, 195)


def test_y2021d12():
    assert get_day_result(YEAR, 12) == (10, 36)


def test_y2021d13():
    assert get_day_result(YEAR, 13) == (
            17,
            '#####\n'
            '#...#\n'
            '#...#\n'
            '#...#\n'
            '#####')


def test_y2021d14():
    assert get_day_result(YEAR, 14) == (1588, 0)
