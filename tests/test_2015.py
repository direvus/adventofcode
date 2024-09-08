import importlib
import os


YEAR = 2015


def get_day_result(day):
    modpath = f'y{YEAR}.d{day:02d}'
    inpath = os.path.join(f'y{YEAR}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result


def test_d01():
    assert get_day_result(1) == (3, 1)


def test_d02():
    assert get_day_result(2) == (58 + 43, 34 + 14)


def test_d03():
    assert get_day_result(3) == (4, 3)


def test_d04():
    assert get_day_result(4) == (609043, 6742839)


def test_d05():
    assert get_day_result(5) == (1, 0)


def test_d06():
    assert get_day_result(6) == (998996, 1001996)


def test_d07():
    assert get_day_result(7) == (65079, 0)


def test_d08():
    assert get_day_result(8) == (12, 19)


def test_d09():
    assert get_day_result(9) == (605, 982)


def test_d10():
    assert get_day_result(10) == (82350, 1166642)


def test_d11():
    assert get_day_result(11) == ('abcdffaa', 'abcdffbb')


def test_d12():
    assert get_day_result(12) == (15, 0)


def test_d13():
    assert get_day_result(13) == (330, 286)


def test_d14():
    assert get_day_result(14) == (1120, 689)


def test_d15():
    assert get_day_result(15) == (62842880, 57600000)
