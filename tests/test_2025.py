from io import StringIO

from tests.common import get_day_result


YEAR = 2025


def test_y2025d01():
    assert get_day_result(YEAR, 1) == (3, 6)


def test_y2025d02():
    assert get_day_result(YEAR, 2) == (1227775554, 4174379265)


def test_y2025d03():
    assert get_day_result(YEAR, 3) == (357, 3121910778619)


def test_y2025d04():
    assert get_day_result(YEAR, 4) == (13, 43)


def test_y2025d05():
    assert get_day_result(YEAR, 5) == (3, 14)


def test_y2025d06():
    assert get_day_result(YEAR, 6) == (4277556, 3263827)


def test_y2025d07():
    assert get_day_result(YEAR, 7) == (21, 40)


def test_y2025d08():
    assert get_day_result(YEAR, 8) == (40, 25272)


def test_y2025d09():
    from y2025.d09 import Grid
    s = StringIO("""
            7,1
            11,1
            11,7
            9,7
            9,5
            2,5
            2,3
            7,3
            """)
    g = Grid()
    g.parse(s)

    assert g.contains_point((0, 0)) is False
    assert g.contains_point((1, 0)) is False
    assert g.contains_point((2, 0)) is False
    assert g.contains_point((3, 0)) is False
    assert g.contains_point((4, 0)) is False
    assert g.contains_point((5, 0)) is False
    assert g.contains_point((6, 0)) is False
    assert g.contains_point((7, 0)) is False
    assert g.contains_point((8, 0)) is False
    assert g.contains_point((9, 0)) is False
    assert g.contains_point((10, 0)) is False
    assert g.contains_point((11, 0)) is False
    assert g.contains_point((12, 0)) is False

    assert g.contains_point((0, 1)) is False
    assert g.contains_point((1, 1)) is False
    assert g.contains_point((2, 1)) is False
    assert g.contains_point((3, 1)) is False
    assert g.contains_point((4, 1)) is False
    assert g.contains_point((5, 1)) is False
    assert g.contains_point((6, 1)) is False
    assert g.contains_point((7, 1)) is True
    assert g.contains_point((8, 1)) is True
    assert g.contains_point((9, 1)) is True
    assert g.contains_point((10, 1)) is True
    assert g.contains_point((11, 1)) is True
    assert g.contains_point((12, 1)) is False

    assert g.contains_point((0, 2)) is False
    assert g.contains_point((1, 2)) is False
    assert g.contains_point((2, 2)) is False
    assert g.contains_point((3, 2)) is False
    assert g.contains_point((4, 2)) is False
    assert g.contains_point((5, 2)) is False
    assert g.contains_point((6, 2)) is False
    assert g.contains_point((7, 2)) is True
    assert g.contains_point((8, 2)) is True
    assert g.contains_point((9, 2)) is True
    assert g.contains_point((10, 2)) is True
    assert g.contains_point((11, 2)) is True
    assert g.contains_point((12, 2)) is False

    assert g.contains_point((0, 3)) is False
    assert g.contains_point((1, 3)) is False
    assert g.contains_point((2, 3)) is True
    assert g.contains_point((3, 3)) is True
    assert g.contains_point((4, 3)) is True
    assert g.contains_point((5, 3)) is True
    assert g.contains_point((6, 3)) is True
    assert g.contains_point((7, 3)) is True
    assert g.contains_point((8, 3)) is True
    assert g.contains_point((9, 3)) is True
    assert g.contains_point((10, 3)) is True
    assert g.contains_point((11, 3)) is True
    assert g.contains_point((12, 3)) is False

    assert g.contains_point((0, 4)) is False
    assert g.contains_point((1, 4)) is False
    assert g.contains_point((2, 4)) is True
    assert g.contains_point((3, 4)) is True
    assert g.contains_point((4, 4)) is True
    assert g.contains_point((5, 4)) is True
    assert g.contains_point((6, 4)) is True
    assert g.contains_point((7, 4)) is True
    assert g.contains_point((8, 4)) is True
    assert g.contains_point((9, 4)) is True
    assert g.contains_point((10, 4)) is True
    assert g.contains_point((11, 4)) is True
    assert g.contains_point((12, 4)) is False

    assert g.contains_point((0, 5)) is False
    assert g.contains_point((1, 5)) is False
    assert g.contains_point((2, 5)) is True
    assert g.contains_point((3, 5)) is True
    assert g.contains_point((4, 5)) is True
    assert g.contains_point((5, 5)) is True
    assert g.contains_point((6, 5)) is True
    assert g.contains_point((7, 5)) is True
    assert g.contains_point((8, 5)) is True
    assert g.contains_point((9, 5)) is True
    assert g.contains_point((10, 5)) is True
    assert g.contains_point((11, 5)) is True
    assert g.contains_point((12, 5)) is False

    assert g.contains_point((0, 6)) is False
    assert g.contains_point((1, 6)) is False
    assert g.contains_point((2, 6)) is False
    assert g.contains_point((3, 6)) is False
    assert g.contains_point((4, 6)) is False
    assert g.contains_point((5, 6)) is False
    assert g.contains_point((6, 6)) is False
    assert g.contains_point((7, 6)) is False
    assert g.contains_point((8, 6)) is False
    assert g.contains_point((9, 6)) is True
    assert g.contains_point((10, 6)) is True
    assert g.contains_point((11, 6)) is True
    assert g.contains_point((12, 6)) is False

    assert g.contains_point((0, 7)) is False
    assert g.contains_point((1, 7)) is False
    assert g.contains_point((2, 7)) is False
    assert g.contains_point((3, 7)) is False
    assert g.contains_point((4, 7)) is False
    assert g.contains_point((5, 7)) is False
    assert g.contains_point((6, 7)) is False
    assert g.contains_point((7, 7)) is False
    assert g.contains_point((8, 7)) is False
    assert g.contains_point((9, 7)) is True
    assert g.contains_point((10, 7)) is True
    assert g.contains_point((11, 7)) is True
    assert g.contains_point((12, 7)) is False

    assert g.contains_point((0, 8)) is False
    assert g.contains_point((1, 8)) is False
    assert g.contains_point((2, 8)) is False
    assert g.contains_point((3, 8)) is False
    assert g.contains_point((4, 8)) is False
    assert g.contains_point((5, 8)) is False
    assert g.contains_point((6, 8)) is False
    assert g.contains_point((7, 8)) is False
    assert g.contains_point((8, 8)) is False
    assert g.contains_point((9, 8)) is False
    assert g.contains_point((10, 8)) is False
    assert g.contains_point((11, 8)) is False
    assert g.contains_point((12, 8)) is False

    assert g.contains_vline((9, 3), (9, 5)) is True
    assert g.contains_vline((9, 3), (9, 7)) is True

    assert g.contains_hline((7, 1), (11, 1)) is True
    assert g.contains_hline((5, 1), (11, 1)) is False
    assert g.contains_hline((2, 3), (11, 3)) is True
    assert g.contains_hline((2, 3), (12, 3)) is False

    assert get_day_result(YEAR, 9) == (50, 24)

def test_y2025d10():
    assert get_day_result(YEAR, 10) == (7, 0)
