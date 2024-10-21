import spans


def test_simplify_spans():
    assert spans.simplify_spans({(1, 3), (2, 4)}) == {(1, 4)}
    assert spans.simplify_spans({(1, 3), (7, 9)}) == {(1, 3), (7, 9)}
    assert spans.simplify_spans({(1, 8), (6, 7)}) == {(1, 8)}
    assert spans.simplify_spans({(1, 8), (1, 5)}) == {(1, 8)}
    assert spans.simplify_spans({(9, 9), (10, 10)}) == {(9, 10)}


def test_subtract_span():
    assert spans.subtract_span((1, 3), (5, 7)) == {(1, 3)}
    assert spans.subtract_span((1, 7), (5, 6)) == {(1, 4), (7, 7)}
    assert spans.subtract_span((1, 7), (6, 7)) == {(1, 5)}
    assert spans.subtract_span((3, 5), (1, 7)) == set()
    assert spans.subtract_span((3, 7), (1, 3)) == {(4, 7)}


def test_subtract_spans():
    assert spans.subtract_spans((1, 7), {(1, 1), (3, 5)}) == {(2, 2), (6, 7)}
