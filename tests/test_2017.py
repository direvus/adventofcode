import importlib
import os


YEAR = 2017


def get_day_result(day):
    modpath = f'y{YEAR}.d{day:02d}'
    inpath = os.path.join(f'y{YEAR}', 'tests', f'{day:02d}')
    m = importlib.import_module(modpath)
    with open(inpath, 'r') as infile:
        result = m.run(infile, test=True)
    return result


def test_y2017d01():
    assert get_day_result(1) == (5, 2)


def test_y2017d02():
    assert get_day_result(2) == (18, 9)


def test_y2017d03():
    from y2017.d03 import find_distance
    assert find_distance(1) == 0
    assert find_distance(12) == 3
    assert find_distance(23) == 2
    assert find_distance(1024) == 31

    assert get_day_result(3) == (31, 1968)


def test_y2017d04():
    assert get_day_result(4) == (7, 5)


def test_y2017d05():
    assert get_day_result(5) == (5, 10)


def test_y2017d06():
    assert get_day_result(6) == (5, 4)


def test_y2017d07():
    assert get_day_result(7) == ('tknk', 60)


def test_y2017d08():
    assert get_day_result(8) == (1, 10)


def test_y2017d09():
    from y2017.d09 import get_total_score, get_garbage_count
    assert get_total_score('{}') == 1
    assert get_total_score('{{{}}}') == 6
    assert get_total_score('{{},{}}') == 5
    assert get_total_score('{{{},{},{{}}}}') == 16
    assert get_total_score('{<a>,<a>,<a>,<a>}') == 1
    assert get_total_score('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
    assert get_total_score('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
    assert get_total_score('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3

    assert get_garbage_count('<>') == 0
    assert get_garbage_count('<random characters>') == 17
    assert get_garbage_count('<<<<>') == 3
    assert get_garbage_count('<{!>}>') == 2
    assert get_garbage_count('<!!>') == 0
    assert get_garbage_count('<!!!>>') == 0
    assert get_garbage_count('<{o"i!a,<{i<a>') == 10

    assert get_day_result(9) == (3, 13)


# def test_y2017d10():
#     assert get_day_result(10) == (0, 0)
#
#
# def test_y2017d11():
#     assert get_day_result(11) == (0, 0)
#
#
# def test_y2017d12():
#     assert get_day_result(12) == (0, 0)
#
#
# def test_y2017d13():
#     assert get_day_result(13) == (0, 0)
#
#
# def test_y2017d14():
#     assert get_day_result(14) == (0, 0)
#
#
# def test_y2017d15():
#     assert get_day_result(15) == (0, 0)
#
#
# def test_y2017d16():
#     assert get_day_result(16) == (0, 0)
#
#
# def test_y2017d17():
#     assert get_day_result(17) == (0, 0)
#
#
# def test_y2017d18():
#     assert get_day_result(18) == (0, 0)
#
#
# def test_y2017d19():
#     assert get_day_result(19) == (0, 0)
#
#
# def test_y2017d20():
#     assert get_day_result(20) == (0, 0)
#
#
# def test_y2017d21():
#     assert get_day_result(21) == (0, 0)
#
#
# def test_y2017d22():
#     assert get_day_result(22) == (0, 0)
#
#
# def test_y2017d23():
#     assert get_day_result(23) == (0, 0)
#
#
# def test_y2017d24():
#     assert get_day_result(24) == (0, 0)
#
#
# def test_y2017d25():
#     assert get_day_result(25) == (0, 0)
