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
    assert get_day_result(3) == (6, 30)


def test_y2019d04():
    from y2019.d04 import is_valid, is_valid2
    assert is_valid('111111') is True
    assert is_valid('122345') is True
    assert is_valid('223450') is False
    assert is_valid('123789') is False
    assert is_valid2('123444') is False
    assert is_valid2('111122') is True
    assert get_day_result(4) == (1385, 981)


def test_y2019d05():
    from y2019.d05 import parse
    comp = parse("3,9,8,9,10,9,4,9,99,-1,8")
    assert comp.run([8]) == (1,)

    comp = parse("3,9,7,9,10,9,4,9,99,-1,8")
    assert comp.run([7]) == (1,)
    comp.reset()
    assert comp.run([8]) == (0,)

    comp = parse("3,3,1108,-1,8,3,4,3,99")
    assert comp.run([9]) == (0,)
    comp.reset()
    assert comp.run([8]) == (1,)

    comp = parse("3,3,1107,-1,8,3,4,3,99")
    assert comp.run([1]) == (1,)
    comp.reset()
    assert comp.run([10]) == (0,)

    comp = parse(
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
            "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
            "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
            )
    assert comp.run([7]) == (999,)
    comp.reset()
    assert comp.run([8]) == (1000,)
    comp.reset()
    assert comp.run([9]) == (1001,)

    assert get_day_result(5) == (1, 5)
