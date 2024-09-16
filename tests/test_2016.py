import importlib
import os


YEAR = 2016


def get_day_result(day):
    modpath = f'y{YEAR}.d{day:02d}'
    inpath = os.path.join(f'y{YEAR}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result


def test_y2016d01():
    assert get_day_result(1) == (8, 4)


def test_y2016d02():
    assert get_day_result(2) == ('1985', '5DB3')


def test_y2016d03():
    assert get_day_result(3) == (3, 6)


def test_y2016d04():
    assert get_day_result(4) == (1857, 'very encrypted name')


def test_y2016d05():
    assert get_day_result(5) == ('18f47a30', '05ace8e3')


def test_y2016d06():
    assert get_day_result(6) == ('easter', 'advent')


def test_y2016d07():
    assert get_day_result(7) == (2, 0)


def test_y2016d08():
    assert get_day_result(8) == (6, 0)


def test_y2016d09():
    assert get_day_result(9) == (57, 56)


def test_y2016d10():
    assert get_day_result(10) == ({1: [2], 2: [3], 0: [5]}, 30)


def test_y2016d11():
    assert get_day_result(11) == (11, 21)


def test_y2016d12():
    assert get_day_result(12) == (42, 42)


def test_y2016d13():
    from y2016.d13 import is_space
    assert is_space(0, 0, 10) is True
    assert is_space(0, 1, 10) is True
    assert is_space(1, 0, 10) is False
    assert is_space(1, 1, 10) is True
    assert is_space(2, 0, 10) is True
    assert is_space(2, 1, 10) is False
    assert get_day_result(13) == (11, 151)


def test_y2016d14():
    assert get_day_result(14) == (22728, 22551)


def test_y2016d15():
    assert get_day_result(15) == (5, 85)


# def test_d16():
#     assert get_day_result(16) == (0, 0)
#
#
# def test_d17():
#     assert get_day_result(17) == (0, 0)
#
#
# def test_d18():
#     assert get_day_result(18) == (0, 0)
#
#
# def test_d19():
#     assert get_day_result(19) == (0, 0)
#
#
# def test_d20():
#     assert get_day_result(20) == (0, 0)
#
#
# def test_d21():
#     assert get_day_result(21) == (0, 0)
#
#
# def test_d22():
#     assert get_day_result(22) == (0, 0)
#
#
# def test_d23():
#     assert get_day_result(23) == (0, 0)
#
#
# def test_d24():
#     assert get_day_result(24) == (0, 0)
#
#
# def test_d25():
#     assert get_day_result(25) == (0, 0)
