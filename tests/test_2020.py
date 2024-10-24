from tests.common import get_day_result


YEAR = 2020


def test_y2020d01():
    assert get_day_result(YEAR, 1) == (514579, 241861950)


def test_y2020d02():
    assert get_day_result(YEAR, 2) == (2, 1)


def test_y2020d03():
    assert get_day_result(YEAR, 3) == (7, 336)


def test_y2020d04():
    assert get_day_result(YEAR, 4) == (2, 2)


def test_y2020d05():
    from y2020.d05 import get_seat

    assert get_seat('FBFBBFFRLR') == (44, 5)
    assert get_day_result(YEAR, 5) == (820, None)


def test_y2020d06():
    assert get_day_result(YEAR, 6) == (11, 6)


def test_y2020d07():
    assert get_day_result(YEAR, 7) == (4, 32)


def test_y2020d08():
    assert get_day_result(YEAR, 8) == (5, 8)


def test_y2020d09():
    assert get_day_result(YEAR, 9) == (127, 62)


def test_y2020d10():
    assert get_day_result(YEAR, 10) == (7 * 5, 8)


def test_y2020d11():
    assert get_day_result(YEAR, 11) == (37, 26)


def test_y2020d12():
    assert get_day_result(YEAR, 12) == (25, 286)


def test_y2020d13():
    assert get_day_result(YEAR, 13) == (295, 1068781)


def test_y2020d14():
    assert get_day_result(YEAR, 14) == (165, 208)


def test_y2020d15():
    assert get_day_result(YEAR, 15) == (436, 0)


def test_y2020d16():
    assert get_day_result(YEAR, 16) == (71, 1)


def test_y2020d17():
    assert get_day_result(YEAR, 17) == (112, 848)


def test_y2020d18():
    from y2020.d18 import tokenise, ArithmeticParser, ArithmeticParser2

    parser = ArithmeticParser(tokenise('2 * 3 + (4 * 5)'))
    assert parser.parse().evaluate() == 26

    parser = ArithmeticParser(tokenise('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert parser.parse().evaluate() == 437

    parser = ArithmeticParser(tokenise(
            '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert parser.parse().evaluate() == 12240

    parser = ArithmeticParser(tokenise(
            '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    assert parser.parse().evaluate() == 13632

    parser = ArithmeticParser2(tokenise(
            '1 + (2 * 3) + (4 * (5 + 6))'))
    assert parser.parse().evaluate() == 51

    parser = ArithmeticParser2(tokenise(
            '2 * 3 + (4 * 5)'))
    assert parser.parse().evaluate() == 46

    parser = ArithmeticParser2(tokenise(
            '5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    assert parser.parse().evaluate() == 1445

    parser = ArithmeticParser2(tokenise(
            '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    assert parser.parse().evaluate() == 669060

    parser = ArithmeticParser2(tokenise(
            '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    assert parser.parse().evaluate() == 23340

    assert get_day_result(YEAR, 18) == (71, 231)


def test_y2020d19():
    assert get_day_result(YEAR, 19) == (3, 12)


def test_y2020d20():
    from y2020.d20 import Tile

    tile = Tile('', '.#.\n..#\n###', 3)
    assert tile.get_edge(0, 0) == (0, 1, 0)
    assert tile.get_edge(1, 0) == (0, 1, 1)
    assert tile.get_edge(2, 0) == (1, 1, 1)
    assert tile.get_edge(3, 0) == (0, 0, 1)

    assert tile.get_edge(0, 1) == (0, 1, 1)
    assert tile.get_edge(1, 1) == (1, 1, 1)
    assert tile.get_edge(2, 1) == (0, 0, 1)
    assert tile.get_edge(3, 1) == (0, 1, 0)

    assert tile.get_edge(0, 2) == (1, 1, 1)
    assert tile.get_edge(1, 2) == (1, 0, 0)
    assert tile.get_edge(2, 2) == (0, 1, 0)
    assert tile.get_edge(3, 2) == (1, 1, 0)

    assert tile.get_edge(0, 3) == (1, 0, 0)
    assert tile.get_edge(1, 3) == (0, 1, 0)
    assert tile.get_edge(2, 3) == (1, 1, 0)
    assert tile.get_edge(3, 3) == (1, 1, 1)

    assert tile.get_edge(0, 4) == (1, 1, 1)
    assert tile.get_edge(1, 4) == (1, 1, 0)
    assert tile.get_edge(2, 4) == (0, 1, 0)
    assert tile.get_edge(3, 4) == (1, 0, 0)

    assert tile.get_edge(0, 5) == (0, 1, 0)
    assert tile.get_edge(1, 5) == (0, 0, 1)
    assert tile.get_edge(2, 5) == (1, 1, 1)
    assert tile.get_edge(3, 5) == (0, 1, 1)

    assert tile.get_edge(0, 6) == (0, 0, 1)
    assert tile.get_edge(1, 6) == (1, 1, 1)
    assert tile.get_edge(2, 6) == (0, 1, 1)
    assert tile.get_edge(3, 6) == (0, 1, 0)

    assert tile.get_edge(0, 7) == (1, 1, 0)
    assert tile.get_edge(1, 7) == (0, 1, 0)
    assert tile.get_edge(2, 7) == (1, 0, 0)
    assert tile.get_edge(3, 7) == (1, 1, 1)

    assert tile.transform(0).pixels == {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
    assert tile.transform(1).pixels == {(1, 0), (2, 0), (0, 1), (2, 1), (2, 2)}
    assert tile.transform(2).pixels == {(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)}
    assert tile.transform(3).pixels == {(0, 0), (0, 1), (2, 1), (0, 2), (1, 2)}
    assert tile.transform(4).pixels == {(0, 0), (1, 0), (2, 0), (2, 1), (1, 2)}
    assert tile.transform(5).pixels == {(1, 0), (0, 1), (0, 2), (1, 2), (2, 2)}
    assert tile.transform(6).pixels == {(2, 0), (0, 1), (2, 1), (1, 2), (2, 2)}
    assert tile.transform(7).pixels == {(0, 0), (1, 0), (0, 1), (2, 1), (0, 2)}

    assert get_day_result(YEAR, 20) == (20899048083289, 273)
