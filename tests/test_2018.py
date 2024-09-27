import importlib
import os


YEAR = 2018


def get_day_result(day):
    modpath = f'y{YEAR}.d{day:02d}'
    inpath = os.path.join(f'y{YEAR}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result


def test_y2018d01():
    assert get_day_result(1) == (3, 2)


def test_y2018d02():
    assert get_day_result(2) == (12, 'abcde')


def test_y2018d03():
    assert get_day_result(3) == (4, 3)


def test_y2018d04():
    assert get_day_result(4) == (240, 4455)


def test_y2018d05():
    assert get_day_result(5) == (10, 4)


def test_y2018d06():
    assert get_day_result(6) == (17, 16)
