from io import StringIO

from tests.common import get_day_result


YEAR = 2018


def test_y2018d01():
    assert get_day_result(YEAR, 1) == (3, 2)


def test_y2018d02():
    assert get_day_result(YEAR, 2) == (12, 'abcde')


def test_y2018d03():
    assert get_day_result(YEAR, 3) == (4, 3)


def test_y2018d04():
    assert get_day_result(YEAR, 4) == (240, 4455)


def test_y2018d05():
    assert get_day_result(YEAR, 5) == (10, 4)


def test_y2018d06():
    assert get_day_result(YEAR, 6) == (17, 16)


def test_y2018d07():
    assert get_day_result(YEAR, 7) == ('CABDFE', 15)


def test_y2018d08():
    assert get_day_result(YEAR, 8) == (138, 66)


def test_y2018d09():
    assert get_day_result(YEAR, 9) == (32, 22563)


def test_y2018d10():
    r1, r2 = get_day_result(YEAR, 10)
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
    assert get_day_result(YEAR, 11) == ((33, 45), (90, 269, 16))


def test_y2018d12():
    assert get_day_result(YEAR, 12) == (325, 999999999374)


def test_y2018d13():
    assert get_day_result(YEAR, 13) == ((7, 3), (6, 4))


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
    assert get_day_result(YEAR, 14) == ('5158916779', 18)


def test_y2018d15():
    from y2018.d15 import Game
    g = Game(
            "#########\n"
            "#G..G..G#\n"
            "#.......#\n"
            "#.......#\n"
            "#G..E..G#\n"
            "#.......#\n"
            "#.......#\n"
            "#G..G..G#\n"
            "#########\n")
    g.do_round()
    assert {x.position for x in g.elves} == {(3, 4)}
    assert {x.position for x in g.goblins} == {
            (1, 2), (1, 6), (2, 4), (3, 7),
            (4, 2), (6, 1), (6, 4), (6, 7)}
    g.do_round()
    assert {x.position for x in g.elves} == {(3, 4)}
    assert {x.position for x in g.goblins} == {
            (1, 3), (1, 5), (2, 4), (3, 6),
            (3, 2), (5, 1), (5, 4), (5, 7)}
    g.do_round()
    assert {x.position for x in g.elves} == {(3, 4)}
    assert {x.position for x in g.goblins} == {
            (2, 3), (2, 4), (2, 5), (3, 3),
            (3, 5), (4, 1), (4, 4), (5, 7)}

    g = Game(
            "#######\n"
            "#G..#E#\n"
            "#E#E.E#\n"
            "#G.##.#\n"
            "#...#E#\n"
            "#...E.#\n"
            "#######\n")
    rounds = g.run()
    assert rounds == 37
    assert g.total_health == 982

    g = Game(
            "#######\n"
            "#E..EG#\n"
            "#.#G.E#\n"
            "#E.##E#\n"
            "#G..#.#\n"
            "#..E#.#\n"
            "#######\n")
    rounds = g.run()
    assert rounds == 46
    assert g.total_health == 859

    g = Game(
            "#######\n"
            "#E.G#.#\n"
            "#.#G..#\n"
            "#G.#.G#\n"
            "#G..#.#\n"
            "#...E.#\n"
            "#######\n")
    rounds = g.run()
    assert rounds == 35
    assert g.total_health == 793

    g = Game(
            "#######\n"
            "#.E...#\n"
            "#.#..G#\n"
            "#.###.#\n"
            "#E#G#G#\n"
            "#...#G#\n"
            "#######\n")
    rounds = g.run()
    assert rounds == 54
    assert g.total_health == 536

    g = Game(
            "#########\n"
            "#G......#\n"
            "#.E.#...#\n"
            "#..##..G#\n"
            "#...##..#\n"
            "#...#...#\n"
            "#.G...G.#\n"
            "#.....G.#\n"
            "#########\n")
    rounds = g.run()
    assert rounds == 20
    assert g.total_health == 937

    assert get_day_result(YEAR, 15) == (27730, 4988)


def test_y2018d16():
    from y2018.d16 import find_matching_instructions
    assert find_matching_instructions(
            (3, 2, 1, 1), (2, 1, 2), (3, 2, 2, 1)) == {'mulr', 'addi', 'seti'}
    assert get_day_result(YEAR, 16) == (1, 0)


def test_y2018d17():
    from y2018.d17 import Grid
    s = StringIO("""x=494, y=3..9
        x=503, y=3..9
        y=9, x=494..503
        x=497, y=5..7
        x=499, y=5..7
        y=5, x=497..499
        y=7, x=497..499
        x=506, y=1..2
        """)
    grid = Grid()
    grid.parse(s)
    grid.do_flow()
    assert grid.count_water() == 66
    assert get_day_result(YEAR, 17) == (57, 29)


def test_y2018d18():
    assert get_day_result(YEAR, 18) == (1147, 0)


def test_y2018d19():
    assert get_day_result(YEAR, 19) == (6, 6)


def test_y2018d20():
    from y2018.d20 import Exp, Graph
    g = Graph()
    g.parse('^WNE$')
    assert g.find_furthest_path() == 3

    e = Exp()
    e.parse('^ENWWW(NEEE|SSE(EE|N))$')
    assert e.nodes == {0: 'ENWWW', 1: 'NEEE', 2: 'SSE', 3: 'EE', 4: 'N', 5: ''}
    assert e.children == {0: {1, 2}, 2: {3, 4}, 3: {5}, 4: {5}}
    g = Graph()
    g.build(e)
    assert g.find_furthest_path() == 10

    g = Graph()
    g.parse('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$')
    assert g.find_furthest_path() == 18

    g = Graph()
    g.parse('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$')
    assert g.find_furthest_path() == 23

    g = Graph()
    g.parse(
            '^WSSEESWWWNW(S|NENNEEEENN'
            '(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')
    assert g.find_furthest_path() == 31

    assert get_day_result(YEAR, 20) == (18, 0)


def test_y2018d21():
    # Nothing really to test with this one.
    assert get_day_result(YEAR, 21) == (0, 0)


def test_y2018d22():
    from y2018.d22 import Grid
    g = Grid(510, (10, 10))
    assert g.get_index((0, 0)) == 0
    assert g.get_level((0, 0)) == 510
    assert g.get_type((0, 0)) == 0

    assert g.get_index((1, 0)) == 16807
    assert g.get_level((1, 0)) == 17317
    assert g.get_type((1, 0)) == 1

    assert g.get_index((0, 1)) == 48271
    assert g.get_level((0, 1)) == 8415
    assert g.get_type((0, 1)) == 0

    assert g.get_index((1, 1)) == 145722555
    assert g.get_level((1, 1)) == 1805
    assert g.get_type((1, 1)) == 2

    assert g.get_index((10, 10)) == 0
    assert g.get_level((10, 10)) == 510
    assert g.get_type((10, 10)) == 0

    assert g.get_risk() == 114

    assert get_day_result(YEAR, 22) == (114, 45)


def test_y2018d23():
    from y2018.d23 import parse
    swarm = parse(
            """
            pos=<10,12,12>, r=2
            pos=<12,14,12>, r=2
            pos=<16,12,12>, r=4
            pos=<14,14,14>, r=6
            pos=<50,50,50>, r=200
            pos=<10,10,10>, r=5
            """)
    assert swarm.count_in_range_of((12, 12, 12)) == 5
    assert get_day_result(YEAR, 23) == (7, 36)


def test_y2018d24():
    assert get_day_result(YEAR, 24) == (5216, 51)


def test_y2018d25():
    from y2018.d25 import parse, count_constellations

    points = parse("""
             0,0,0,0
             3,0,0,0
             0,3,0,0
             0,0,3,0
             0,0,0,3
             0,0,0,6
             9,0,0,0
            12,0,0,0
            """)
    assert count_constellations(points) == 2

    points = parse("""
            -1,2,2,0
            0,0,2,-2
            0,0,0,-2
            -1,2,0,0
            -2,-2,-2,2
            3,0,2,-1
            -1,3,2,2
            -1,0,-1,0
            0,2,1,-2
            3,0,0,0
            """)
    assert count_constellations(points) == 4

    points = parse("""
            1,-1,0,1
            2,0,-1,0
            3,2,-1,0
            0,0,3,1
            0,0,-1,-1
            2,3,-2,0
            -2,2,0,0
            2,-2,0,-1
            1,-1,0,-1
            3,2,0,2
            """)
    assert count_constellations(points) == 3

    points = parse("""
            1,-1,-1,-2
            -2,-2,0,1
            0,2,1,3
            -2,3,-2,1
            0,2,3,-2
            -1,-1,1,-2
            0,-2,-1,0
            -2,2,3,-1
            1,2,2,0
            -1,-2,0,-2
            """)
    assert count_constellations(points) == 8

    assert get_day_result(YEAR, 25) == (4, 0)
