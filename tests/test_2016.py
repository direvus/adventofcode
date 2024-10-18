from tests.common import get_day_result


YEAR = 2016


def test_y2016d01():
    assert get_day_result(YEAR, 1) == (8, 4)


def test_y2016d02():
    assert get_day_result(YEAR, 2) == ('1985', '5DB3')


def test_y2016d03():
    assert get_day_result(YEAR, 3) == (3, 6)


def test_y2016d04():
    assert get_day_result(YEAR, 4) == (1857, 'very encrypted name')


def test_y2016d05():
    assert get_day_result(YEAR, 5) == ('18f47a30', '05ace8e3')


def test_y2016d06():
    assert get_day_result(YEAR, 6) == ('easter', 'advent')


def test_y2016d07():
    assert get_day_result(YEAR, 7) == (2, 0)


def test_y2016d08():
    assert get_day_result(YEAR, 8) == (6, 0)


def test_y2016d09():
    assert get_day_result(YEAR, 9) == (57, 56)


def test_y2016d10():
    assert get_day_result(YEAR, 10) == ({1: [2], 2: [3], 0: [5]}, 30)


def test_y2016d11():
    assert get_day_result(YEAR, 11) == (11, 21)


def test_y2016d12():
    assert get_day_result(YEAR, 12) == (42, 42)


def test_y2016d13():
    from y2016.d13 import is_space
    assert is_space(0, 0, 10) is True
    assert is_space(0, 1, 10) is True
    assert is_space(1, 0, 10) is False
    assert is_space(1, 1, 10) is True
    assert is_space(2, 0, 10) is True
    assert is_space(2, 1, 10) is False
    assert get_day_result(YEAR, 13) == (11, 151)


def test_y2016d14():
    assert get_day_result(YEAR, 14) == (22728, 22551)


def test_y2016d15():
    assert get_day_result(YEAR, 15) == (5, 85)


def test_y2016d16():
    assert get_day_result(YEAR, 16) == ('01100', '0000100010100000110010100')


def test_y2016d17():
    assert get_day_result(YEAR, 17) == ('DDRRRD', 370)


def test_y2016d18():
    assert get_day_result(YEAR, 18) == (38, 1935478)


def test_y2016d19():
    from y2016.d19 import get_winner_p2
    assert get_winner_p2(2) == 1
    assert get_winner_p2(3) == 3
    assert get_winner_p2(4) == 1
    assert get_winner_p2(5) == 2
    assert get_winner_p2(6) == 3
    assert get_winner_p2(7) == 5
    assert get_winner_p2(8) == 7
    assert get_winner_p2(9) == 9
    assert get_winner_p2(10) == 1
    assert get_winner_p2(11) == 2
    assert get_winner_p2(12) == 3
    assert get_day_result(YEAR, 19) == (3, 2)


def test_y2016d20():
    assert get_day_result(YEAR, 20) == (3, 5)


def test_y2016d21():
    from y2016.d21 import (
            swap_position, swap_letter, rotate_count,
            rotate_index, reverse_span, move_index,
            )
    assert swap_position('abcde', 4, 0) == 'ebcda'
    assert swap_letter('ebcda', 'd', 'b') == 'edcba'
    assert rotate_count('abcde', 1) == 'eabcd'
    assert rotate_count('abcde', 2) == 'deabc'
    assert rotate_count('abcde', -1) == 'bcdea'
    assert rotate_index('ecabd', 'd') == 'decab'
    assert reverse_span('abcde', 0, 4) == 'edcba'
    assert reverse_span('abcde', 1, 3) == 'adcbe'
    assert move_index('bcdea', 1, 4) == 'bdeac'
    assert get_day_result(YEAR, 21) == ('fbdecgha', 'abcdefgh')


def test_y2016d22():
    assert get_day_result(YEAR, 22) == (7, 7)


def test_y2016d23():
    assert get_day_result(YEAR, 23) == (3, 479009420)


def test_y2016d24():
    assert get_day_result(YEAR, 24) == (14, 20)


def test_y2016d25():
    assert get_day_result(YEAR, 25) == (196, None)
