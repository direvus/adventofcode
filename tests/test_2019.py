import importlib
import os


YEAR = 2019


def get_day_result(day):
    modpath = f'y{YEAR}.d{day:02d}'
    inpath = os.path.join(f'y{YEAR}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result


def test_y2019d01():
    from y2019.d01 import get_total_fuel_nested
    assert get_total_fuel_nested([14]) == 2
    assert get_total_fuel_nested([1969]) == 966
    assert get_total_fuel_nested([100756]) == 50346
    assert get_day_result(1) == (34241, 51316)


def test_y2019d02():
    assert get_day_result(2) == (3500, 0)


def test_y2019d03():
    assert get_day_result(3) == (6, 0)
