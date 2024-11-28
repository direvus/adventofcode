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


def test_y2022d07():
    assert get_day_result(YEAR, 7) == (95437, 24933642)


def test_y2022d08():
    assert get_day_result(YEAR, 8) == (21, 8)


def test_y2022d09():
    assert get_day_result(YEAR, 9) == (13, 1)


def test_y2022d10():
    result2 = (
            '##..##..##..##..##..##..##..##..##..##..\n'
            '###...###...###...###...###...###...###.\n'
            '####....####....####....####....####....\n'
            '#####.....#####.....#####.....#####.....\n'
            '######......######......######......####\n'
            '#######.......#######.......#######.....'
            )
    assert get_day_result(YEAR, 10) == (13140, result2)


def test_y2022d11():
    assert get_day_result(YEAR, 11) == (10605, 2713310158)


def test_y2022d12():
    assert get_day_result(YEAR, 12) == (31, 29)


def test_y2022d13():
    assert get_day_result(YEAR, 13) == (13, 140)


def test_y2022d14():
    assert get_day_result(YEAR, 14) == (24, 93)


def test_y2022d15():
    assert get_day_result(YEAR, 15) == (26, 56000011)


def test_y2022d16():
    assert get_day_result(YEAR, 16) == (1651, 1707)


def test_y2022d17():
    assert get_day_result(YEAR, 17) == (3068, 1514285714288)


def test_y2022d18():
    assert get_day_result(YEAR, 18) == (64, 58)


def test_y2022d19():
    assert get_day_result(YEAR, 19) == (33, 0)


def test_y2022d20():
    assert get_day_result(YEAR, 20) == (3, 1623178306)
