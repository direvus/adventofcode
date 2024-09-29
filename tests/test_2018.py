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


def test_y2018d07():
    assert get_day_result(7) == ('CABDFE', 15)


def test_y2018d08():
    assert get_day_result(8) == (138, 66)


def test_y2018d09():
    assert get_day_result(9) == (32, 22563)


def test_y2018d10():
    r1, r2 = get_day_result(10)
    assert r1 == (
            '............\n'
            '.#...#..###.\n'
            '.#...#...#..\n'
            '.#...#...#..\n'
            '.#####...#..\n'
            '.#...#...#..\n'
            '.#...#...#..\n'
            '.#...#...#..\n'
            '.#...#..###.\n'
            '............')
    assert r2 == 3


def test_y2018d11():
    from y2018.d11 import Grid
    assert Grid(8).get_power_level((3, 5)) == 4
    assert Grid(57).get_power_level((122, 79)) == -5
    assert Grid(39).get_power_level((217, 196)) == 0
    assert Grid(71).get_power_level((101, 153)) == 4
    assert Grid(42).get_square_power((21, 61), 3) == 30
    assert get_day_result(11) == ((33, 45), (90, 269, 16))


def test_y2018d12():
    assert get_day_result(12) == (325, 999999999374)


def test_y2018d13():
    assert get_day_result(13) == ((7, 3), (6, 4))


def test_y2018d14():
    from y2018.d14 import Board
    board = Board((3, 7), (0, 1))
    board.get_scores(5, 10) == (0, 1, 2, 4, 5, 1, 5, 8, 9, 1)
    board.get_scores(18, 10) == (9, 2, 5, 1, 0, 7, 1, 0, 8, 5)
    board.get_scores(2018, 10) == (5, 9, 4, 1, 4, 2, 9, 8, 8, 2)

    Board((3, 7), (0, 1)).get_count_before(51589) == 9
    Board((3, 7), (0, 1)).get_count_before('01245') == 5
    Board((3, 7), (0, 1)).get_count_before(92510) == 18
    Board((3, 7), (0, 1)).get_count_before(59414) == 2018
    assert get_day_result(14) == ('5158916779', 18)
