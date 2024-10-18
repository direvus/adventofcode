from tests.common import get_day_result


YEAR = 2015


def test_y2015d01():
    assert get_day_result(YEAR, 1) == (3, 1)


def test_y2015d02():
    assert get_day_result(YEAR, 2) == (58 + 43, 34 + 14)


def test_y2015d03():
    assert get_day_result(YEAR, 3) == (4, 3)


def test_y2015d04():
    assert get_day_result(YEAR, 4) == (609043, 6742839)


def test_y2015d05():
    assert get_day_result(YEAR, 5) == (1, 0)


def test_y2015d06():
    assert get_day_result(YEAR, 6) == (998996, 1001996)


def test_y2015d07():
    assert get_day_result(YEAR, 7) == (65079, 0)


def test_y2015d08():
    assert get_day_result(YEAR, 8) == (12, 19)


def test_y2015d09():
    assert get_day_result(YEAR, 9) == (605, 982)


def test_y2015d10():
    assert get_day_result(YEAR, 10) == (82350, 1166642)


def test_y2015d11():
    assert get_day_result(YEAR, 11) == ('abcdffaa', 'abcdffbb')


def test_y2015d12():
    assert get_day_result(YEAR, 12) == (15, 0)


def test_y2015d13():
    assert get_day_result(YEAR, 13) == (330, 286)


def test_y2015d14():
    assert get_day_result(YEAR, 14) == (1120, 689)


def test_y2015d15():
    assert get_day_result(YEAR, 15) == (62842880, 57600000)


def test_y2015d16():
    assert get_day_result(YEAR, 16) == (5, 4)


def test_y2015d17():
    assert get_day_result(YEAR, 17) == (4, 3)


def test_y2015d18():
    assert get_day_result(YEAR, 18) == (4, 17)


def test_y2015d19():
    assert get_day_result(YEAR, 19) == (7, 6)


def test_y2015d20():
    assert get_day_result(YEAR, 20) == (6, 6)


def test_y2015d21():
    assert get_day_result(YEAR, 21) == ((0, 2, 7), 0)


def test_y2015d22():
    assert get_day_result(YEAR, 22) == ((True, -1, 1, 9), 392)


def test_y2015d23():
    assert get_day_result(YEAR, 23) == (2, 7)


def test_y2015d24():
    assert get_day_result(YEAR, 24) == (99, 44)


def test_y2015d25():
    assert get_day_result(YEAR, 25) == (31663883, 0)
