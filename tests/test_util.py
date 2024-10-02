import util


def test_is_prime():
    assert util.is_prime(2) is True
    assert util.is_prime(3) is True
    assert util.is_prime(4) is False
    assert util.is_prime(5) is True
    assert util.is_prime(6) is False
    assert util.is_prime(7) is True
    assert util.is_prime(8) is False
    assert util.is_prime(9) is False
    assert util.is_prime(10) is False


def test_get_divisors():
    assert util.get_divisors(1) == {1}
    assert util.get_divisors(2) == {1, 2}
    assert util.get_divisors(3) == {1, 3}
    assert util.get_divisors(4) == {1, 2, 4}
    assert util.get_divisors(12) == {1, 2, 3, 4, 6, 12}


def test_get_digits():
    assert util.get_digits(0) == (0,)
    assert util.get_digits(1) == (1,)
    assert util.get_digits(10) == (1, 0)
    assert util.get_digits(3548915) == (3, 5, 4, 8, 9, 1, 5)
