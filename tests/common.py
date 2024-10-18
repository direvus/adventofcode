import os
import importlib


def get_day_result(year, day):
    modpath = f'y{year}.d{day:02d}'
    inpath = os.path.join(f'y{year}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result
