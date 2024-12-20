from tests.common import get_day_result


YEAR = 2017


def test_y2017d01():
    assert get_day_result(YEAR, 1) == (5, 2)


def test_y2017d02():
    assert get_day_result(YEAR, 2) == (18, 9)


def test_y2017d03():
    from y2017.d03 import find_distance
    assert find_distance(1) == 0
    assert find_distance(12) == 3
    assert find_distance(23) == 2
    assert find_distance(1024) == 31

    assert get_day_result(YEAR, 3) == (31, 1968)


def test_y2017d04():
    assert get_day_result(YEAR, 4) == (7, 5)


def test_y2017d05():
    assert get_day_result(YEAR, 5) == (5, 10)


def test_y2017d06():
    assert get_day_result(YEAR, 6) == (5, 4)


def test_y2017d07():
    assert get_day_result(YEAR, 7) == ('tknk', 60)


def test_y2017d08():
    assert get_day_result(YEAR, 8) == (1, 10)


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

    assert get_day_result(YEAR, 9) == (3, 13)


def test_y2017d10():
    from y2017.d10 import get_hash
    assert get_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
    assert get_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
    assert get_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
    assert get_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'

    assert get_day_result(YEAR, 10) == (12, '4a19451b02fb05416d73aea0ec8c00c0')


def test_y2017d11():
    from y2017.d11 import get_path_distance
    assert get_path_distance('ne,ne,ne'.split(',')) == 3
    assert get_path_distance('ne,ne,sw,sw'.split(',')) == 0
    assert get_path_distance('ne,ne,s,s'.split(',')) == 2
    assert get_path_distance('se,sw,se,sw,sw'.split(',')) == 3
    assert get_day_result(YEAR, 11) == (3, 3)


def test_y2017d12():
    assert get_day_result(YEAR, 12) == (6, 2)


def test_y2017d13():
    assert get_day_result(YEAR, 13) == (24, 10)


def test_y2017d14():
    assert get_day_result(YEAR, 14) == (8108, 1242)


def test_y2017d15():
    from y2017.d15 import get_generators, match16
    a, b = get_generators(65, 8921)
    assert a.next() == 1092455
    assert b.next() == 430625591
    assert a.next() == 1181022009
    assert b.next() == 1233683848
    assert a.next() == 245556042
    assert b.next() == 1431495498
    assert a.next() == 1744312007
    assert b.next() == 137874439
    assert a.next() == 1352636452
    assert b.next() == 285222916

    assert match16(1092455, 430625591) is False
    assert match16(1181022009, 1233683848) is False
    assert match16(245556042, 1431495498) is True

    assert get_day_result(YEAR, 15) == (588, 309)


def test_y2017d16():
    assert get_day_result(YEAR, 16) == ('baedc', 'abcde')


def test_y2017d17():
    assert get_day_result(YEAR, 17) == (638, 1222153)


def test_y2017d18():
    assert get_day_result(YEAR, 18) == (4, 3)


def test_y2017d19():
    assert get_day_result(YEAR, 19) == ('ABCDEF', 38)


def test_y2017d20():
    assert get_day_result(YEAR, 20) == (0, 2)


def test_y2017d21():
    assert get_day_result(YEAR, 21) == (12, 0)


def test_y2017d22():
    assert get_day_result(YEAR, 22) == (5587, 26)


def test_y2017d23():
    assert get_day_result(YEAR, 23) == (2, 903)


def test_y2017d24():
    assert get_day_result(YEAR, 24) == (31, 19)


def test_y2017d25():
    assert get_day_result(YEAR, 25) == (3, 0)
