import unittest

from tests.common import get_day_result


class TestSolutions2023(unittest.TestCase):
    year = 2023

    def test_y2023d01(self):
        assert get_day_result(self.year, 1) == (142, 142)

    def test_y2023d02(self):
        assert get_day_result(self.year, 2) == (8, 2286)

    def test_y2023d03(self):
        assert get_day_result(self.year, 3) == (4361, 467835)

    def test_y2023d04(self):
        assert get_day_result(self.year, 4) == (13, 30)

    def test_y2023d05(self):
        assert get_day_result(self.year, 5) == (35, 46)

    def test_y2023d06(self):
        assert get_day_result(self.year, 6) == (288, 71503)

    def test_y2023d07(self):
        assert get_day_result(self.year, 7) == (6440, 5905)

    def test_y2023d08(self):
        assert get_day_result(self.year, 8) == (2, 2)

    def test_y2023d09(self):
        assert get_day_result(self.year, 9) == (114, 2)

    def test_y2023d10(self):
        assert get_day_result(self.year, 10) == (8, 1)

    def test_y2023d11(self):
        assert get_day_result(self.year, 11) == (374, 82000210)

    def test_y2023d12(self):
        assert get_day_result(self.year, 12) == (21, 525152)

    def test_y2023d13(self):
        assert get_day_result(self.year, 13) == (405, 400)

    def test_y2023d14(self):
        assert get_day_result(self.year, 14) == (136, 64)

    def test_y2023d15(self):
        assert get_day_result(self.year, 15) == (1320, 145)

    def test_y2023d16(self):
        assert get_day_result(self.year, 16) == (46, 51)

    def test_y2023d17(self):
        assert get_day_result(self.year, 17) == (102, 94)

    def test_y2023d18(self):
        assert get_day_result(self.year, 18) == (62, 952408144115)

    def test_y2023d19(self):
        assert get_day_result(self.year, 19) == (19114, 167409079868000)

    def test_y2023d20(self):
        assert get_day_result(self.year, 20) == (32000000, 247023644760071)

    def test_y2023d21(self):
        assert get_day_result(self.year, 21) == (16, 7053)

    def test_y2023d22(self):
        assert get_day_result(self.year, 22) == (5, 7)

    def test_y2023d23(self):
        assert get_day_result(self.year, 23) == (94, 154)

    def test_y2023d24(self):
        assert get_day_result(self.year, 24) == (2, 47)

    def test_y2023d25(self):
        assert get_day_result(self.year, 25) == (54, None)
