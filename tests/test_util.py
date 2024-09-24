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
