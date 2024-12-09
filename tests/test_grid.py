import grid


def test_in_bound():
    w = 3
    h = 2
    results = tuple(
            grid.in_bound(w, h, (x, y))
            for y in range(-1, h + 1)
            for x in range(-1, w + 1))
    assert results == (
            False, False, False, False, False,
            False, True, True, True, False,
            False, True, True, True, False,
            False, False, False, False, False,
            )


def test_adjacent():
    assert grid.get_adjacent((0, 0)) == {(0, -1), (1, 0), (0, 1), (-1, 0)}
    assert grid.get_adjacent((3, 2)) == {(3, 1), (3, 3), (2, 2), (4, 2)}
    assert grid.get_adjacent((-1, 1)) == {(-1, 2), (-1, 0), (0, 1), (-2, 1)}


def test_move():
    assert grid.move((0, 0), 0, 1) == (0, -1)
    assert grid.move((0, 0), 1, 1) == (1, 0)
    assert grid.move((0, 0), 2, 1) == (0, 1)
    assert grid.move((0, 0), 3, 1) == (-1, 0)

    assert grid.move((-1, 2), 0, 1) == (-1, 1)
    assert grid.move((-1, 2), 1, 1) == (0, 2)
    assert grid.move((-1, 2), 2, 1) == (-1, 3)
    assert grid.move((-1, 2), 3, 1) == (-2, 2)

    assert grid.move((0, 0), 1, 5) == (5, 0)


def test_turn():
    assert grid.turn(0, 1) == 1
    assert grid.turn(0, 2) == 2
    assert grid.turn(0, 3) == 3
    assert grid.turn(0, 4) == 0
    assert grid.turn(0, 5) == 1
    assert grid.turn(0, -1) == 3
    assert grid.turn(0, -2) == 2
    assert grid.turn(0, -3) == 1
    assert grid.turn(0, -4) == 0


def test_distance():
    assert grid.get_distance((0, 0), (0, 0)) == 0
    assert grid.get_distance((0, 0), (1, 1)) == 2
    assert grid.get_distance((9, 6), (10, 6)) == 1
    assert grid.get_distance((-3, 2), (3, 3)) == 7


def test_parse():
    g = grid.Grid().parse(['abc', 'def'])
    assert g.cells == [['a', 'b', 'c'], ['d', 'e', 'f']]
    assert g.width == 3
    assert g.height == 2


def test_bounded_adjacent():
    g = grid.Grid().parse(['abc', 'def'])
    assert g.get_adjacent((0, 0)) == {(1, 0), (0, 1)}
    assert g.get_adjacent((0, 1)) == {(0, 0), (1, 1)}
    assert g.get_adjacent((2, 0)) == {(1, 0), (2, 1)}
    assert g.get_adjacent((2, 1)) == {(1, 1), (2, 0)}


def test_sparse_parse():
    g = grid.SparseGrid().parse(['.#.', '..#', '...'])
    assert g.cells == {(1, 0), (2, 1)}
    assert g.width == 3
    assert g.height == 3
