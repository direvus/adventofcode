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
