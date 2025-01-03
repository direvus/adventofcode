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


def test_y2024d16():
    assert get_day_result(YEAR, 16) == (7036, 45)


def test_y2024d17():
    assert get_day_result(YEAR, 17) == ('4,6,3,5,6,3,5,2,1,0', 117440)


def test_y2024d18():
    assert get_day_result(YEAR, 18) == (22, '6,1')


def test_y2024d19():
    assert get_day_result(YEAR, 19) == (6, 16)


def test_y2024d20():
    assert get_day_result(YEAR, 20) == (1, 285)


def test_y2024d21():
    assert get_day_result(YEAR, 21) == (126384, 154115708116294)


def test_y2024d22():
    assert get_day_result(YEAR, 22) == (37327623, 23)


def test_y2024d23():
    assert get_day_result(YEAR, 23) == (7, 'co,de,ka,ta')


def test_y2024d24():
    assert get_day_result(YEAR, 24) == (4, 0)


def test_y2024d25():
    assert get_day_result(YEAR, 25) == (3, 0)
