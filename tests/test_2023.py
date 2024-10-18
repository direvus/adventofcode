from tests.common import get_day_result


YEAR = 2023


def test_y2023d01():
    assert get_day_result(YEAR, 1) == (142, 142)


def test_y2023d02():
    assert get_day_result(YEAR, 2) == (8, 2286)


def test_y2023d03():
    assert get_day_result(YEAR, 3) == (4361, 467835)


def test_y2023d04():
    assert get_day_result(YEAR, 4) == (13, 30)


def test_y2023d05():
    assert get_day_result(YEAR, 5) == (35, 46)


def test_y2023d06():
    assert get_day_result(YEAR, 6) == (288, 71503)


def test_y2023d07():
    assert get_day_result(YEAR, 7) == (6440, 5905)


def test_y2023d08():
    assert get_day_result(YEAR, 8) == (2, 2)


def test_y2023d09():
    assert get_day_result(YEAR, 9) == (114, 2)


def test_y2023d10():
    assert get_day_result(YEAR, 10) == (8, 1)


def test_y2023d11():
    assert get_day_result(YEAR, 11) == (374, 82000210)


def test_y2023d12():
    assert get_day_result(YEAR, 12) == (21, 525152)


def test_y2023d13():
    assert get_day_result(YEAR, 13) == (405, 400)


def test_y2023d14():
    assert get_day_result(YEAR, 14) == (136, 64)


def test_y2023d15():
    assert get_day_result(YEAR, 15) == (1320, 145)


def test_y2023d16():
    assert get_day_result(YEAR, 16) == (46, 51)


def test_y2023d17():
    assert get_day_result(YEAR, 17) == (102, 94)


def test_y2023d18():
    assert get_day_result(YEAR, 18) == (62, 952408144115)


def test_y2023d19():
    assert get_day_result(YEAR, 19) == (19114, 167409079868000)


def test_y2023d20():
    assert get_day_result(YEAR, 20) == (32000000, 247023644760071)


def test_y2023d21():
    assert get_day_result(YEAR, 21) == (16, 7053)


def test_y2023d22():
    assert get_day_result(YEAR, 22) == (5, 7)


def test_y2023d23():
    assert get_day_result(YEAR, 23) == (94, 154)


def test_y2023d24():
    assert get_day_result(YEAR, 24) == (2, 47)


def test_y2023d25():
    assert get_day_result(YEAR, 25) == (54, None)
