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


def test_d01():
    assert get_day_result(1) == (8, 4)


def test_d02():
    assert get_day_result(2) == ('1985', '5DB3')


def test_d03():
    assert get_day_result(3) == (3, 6)


def test_d04():
    assert get_day_result(4) == (1857, 'very encrypted name')


def test_d05():
    assert get_day_result(5) == ('18f47a30', 0)


# def test_d06():
#     assert get_day_result(6) == (0, 0)
#
#
# def test_d07():
#     assert get_day_result(7) == (0, 0)
#
#
# def test_d08():
#     assert get_day_result(8) == (0, 0)
#
#
# def test_d09():
#     assert get_day_result(9) == (0, 0)
#
#
# def test_d10():
#     assert get_day_result(10) == (0, 0)
#
#
# def test_d11():
#     assert get_day_result(11) == (0, 0)
#
#
# def test_d12():
#     assert get_day_result(12) == (0, 0)
#
#
# def test_d13():
#     assert get_day_result(13) == (0, 0)
#
#
# def test_d14():
#     assert get_day_result(14) == (0, 0)
#
#
# def test_d15():
#     assert get_day_result(15) == (0, 0)
#
#
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
