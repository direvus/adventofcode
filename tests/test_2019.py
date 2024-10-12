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


def test_y2019d13():
    assert get_day_result(13) == (0, 0)


def test_y2019d14():
    from y2019.d14 import Graph

    g = Graph("""
            9 ORE => 2 A
            8 ORE => 3 B
            7 ORE => 5 C
            3 A, 4 B => 1 AB
            5 B, 7 C => 1 BC
            4 C, 1 A => 1 CA
            2 AB, 3 BC, 4 CA => 1 FUEL
            """)
    assert g.find_ore_required('FUEL') == 165

    g = Graph("""
            157 ORE => 5 NZVS
            165 ORE => 6 DCFZ
            44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
            12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
            179 ORE => 7 PSHF
            177 ORE => 5 HKGWZ
            7 DCFZ, 7 PSHF => 2 XJWVT
            165 ORE => 2 GPVTF
            3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
            """)
    assert g.find_ore_required('FUEL') == 13312
    assert g.get_fuel(10 ** 12) == 82892753

    g = Graph("""
            2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
            17 NVRVD, 3 JNWZP => 8 VPVL
            53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
            22 VJHF, 37 MNCFX => 5 FWMGM
            139 ORE => 4 NVRVD
            144 ORE => 7 JNWZP
            5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
            5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
            145 ORE => 6 MNCFX
            1 NVRVD => 8 CXFTF
            1 VJHF, 6 MNCFX => 4 RFSQX
            176 ORE => 6 VJHF
            """)
    assert g.find_ore_required('FUEL') == 180697
    assert g.get_fuel(10 ** 12) == 5586022

    g = Graph("""
            171 ORE => 8 CNZTR
            7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
            114 ORE => 4 BHXH
            14 VRPVC => 6 BMBT
            6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
            6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
            15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
            13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
            5 BMBT => 4 WPTQ
            189 ORE => 9 KTJDG
            1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
            12 VRPVC, 27 CNZTR => 2 XDBXC
            15 KTJDG, 12 BHXH => 5 XCVML
            3 BHXH, 2 VRPVC => 7 MZWV
            121 ORE => 7 VRPVC
            7 XCVML => 6 RJRHP
            5 BHXH, 4 VRPVC => 5 LTCX
            """)
    assert g.find_ore_required('FUEL') == 2210736
    assert g.get_fuel(10 ** 12) == 460664

    assert get_day_result(14) == (31, 34482758620)


def test_y2019d15():
    assert get_day_result(15) == (0, 0)


def test_y2019d16():
    from y2019.d16 import get_element, get_slices, do_phase
    inputs = (1, 2, 3, 4, 5, 6, 7, 8)
    assert get_slices(8, 1) == ([slice(1, 3)], [slice(5, 7)])
    assert get_element(inputs, 0) == 4
    assert get_element(inputs, 1) == 8
    assert get_element(inputs, 2) == 2
    assert get_element(inputs, 3) == 2
    assert get_element(inputs, 4) == 6
    assert get_element(inputs, 5) == 1
    assert get_element(inputs, 6) == 5
    assert get_element(inputs, 7) == 8
    signal = do_phase(inputs)
    assert signal == (4, 8, 2, 2, 6, 1, 5, 8)
    signal = do_phase(signal)
    assert signal == (3, 4, 0, 4, 0, 4, 3, 8)
    signal = do_phase(signal)
    assert signal == (0, 3, 4, 1, 5, 5, 1, 8)
    signal = do_phase(signal)
    assert signal == (0, 1, 0, 2, 9, 4, 9, 8)
    assert get_day_result(16) == ('24176176', '84462026')
