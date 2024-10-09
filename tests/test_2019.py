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


def test_y2019d06():
    assert get_day_result(6) == (42, 4)


def test_y2019d07():
    from y2019.d07 import parse
    chain = parse(
            "3,23,3,24,1002,24,10,24,1002,23,-1,23,"
            "101,5,23,23,1,24,23,23,4,23,99,0,0")
    assert chain.run((0, 1, 2, 3, 4)) == 54321

    chain = parse(
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
            "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")
    assert chain.run((1, 0, 4, 3, 2)) == 65210

    chain = parse(
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
            "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
    assert chain.run_loop((9, 8, 7, 6, 5)) == 139629729
    assert get_day_result(7) == (43210, 139629729)


def test_y2019d08():
    assert get_day_result(8) == (1, ' *\n* ')


def test_y2019d09():
    from y2019.intcode import Computer
    prog = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    comp = Computer(prog)
    assert comp.run() == comp.program

    comp = Computer("1102,34915192,34915192,7,4,7,99,0")
    assert comp.run() == (1219070632396864,)

    comp = Computer("104,1125899906842624,99")
    assert comp.run() == (1125899906842624,)

    assert get_day_result(9) == (prog, prog)


def test_y2019d10():
    assert get_day_result(10) == (210, 802)


def test_y2019d11():
    assert get_day_result(11) == (0, 0)


def test_y2019d12():
    assert get_day_result(12) == (179, 2772)
