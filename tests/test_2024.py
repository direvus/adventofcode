import unittest

from tests.common import get_day_result


class TestSolutions2024(unittest.TestCase):
    year = 2024

    def test_y2024d01(self):
        assert get_day_result(self.year, 1) == (11, 31)

    def test_y2024d02(self):
        assert get_day_result(self.year, 2) == (2, 4)

    def test_y2024d03(self):
        assert get_day_result(self.year, 3) == (161, 48)

    def test_y2024d04(self):
        assert get_day_result(self.year, 4) == (18, 9)

    def test_y2024d05(self):
        assert get_day_result(self.year, 5) == (143, 123)

    def test_y2024d06(self):
        assert get_day_result(self.year, 6) == (41, 6)

    def test_y2024d07(self):
        assert get_day_result(self.year, 7) == (3749, 11387)

    def test_y2024d08(self):
        assert get_day_result(self.year, 8) == (14, 34)

    def test_y2024d09(self):
        assert get_day_result(self.year, 9) == (1928, 2858)

    def test_y2024d10(self):
        assert get_day_result(self.year, 10) == (36, 81)

    def test_y2024d11(self):
        assert get_day_result(self.year, 11) == (55312, 65601038650482)

    def test_y2024d12(self):
        assert get_day_result(self.year, 12) == (1930, 1206)

    def test_y2024d13(self):
        assert get_day_result(self.year, 13) == (480, 875318608908)

    def test_y2024d14(self):
        assert get_day_result(self.year, 14) == (12, 0)

    def test_y2024d15(self):
        assert get_day_result(self.year, 15) == (10092, 9021)

    def test_y2024d16(self):
        assert get_day_result(self.year, 16) == (7036, 45)

    def test_y2024d17(self):
        assert get_day_result(self.year, 17) == ('4,6,3,5,6,3,5,2,1,0', 117440)

    def test_y2024d18(self):
        assert get_day_result(self.year, 18) == (22, '6,1')

    def test_y2024d19(self):
        assert get_day_result(self.year, 19) == (6, 16)

    def test_y2024d20(self):
        assert get_day_result(self.year, 20) == (1, 285)

    def test_y2024d21(self):
        assert get_day_result(self.year, 21) == (126384, 154115708116294)

    def test_y2024d22(self):
        assert get_day_result(self.year, 22) == (37327623, 23)

    def test_y2024d23(self):
        assert get_day_result(self.year, 23) == (7, 'co,de,ka,ta')

    def test_y2024d24(self):
        assert get_day_result(self.year, 24) == (4, 0)

    def test_y2024d25(self):
        assert get_day_result(self.year, 25) == (3, 0)
