import unittest

from tests.common import get_day_result


class TestSolutions2022(unittest.TestCase):
    year = 2022

    def test_y2022d01(self):
        assert get_day_result(self.year, 1) == (24000, 45000)

    def test_y2022d02(self):
        assert get_day_result(self.year, 2) == (15, 12)

    def test_y2022d03(self):
        assert get_day_result(self.year, 3) == (157, 70)

    def test_y2022d04(self):
        assert get_day_result(self.year, 4) == (2, 4)

    def test_y2022d05(self):
        assert get_day_result(self.year, 5) == ('CMZ', 'MCD')

    def test_y2022d06(self):
        assert get_day_result(self.year, 6) == (7, 19)

    def test_y2022d07(self):
        assert get_day_result(self.year, 7) == (95437, 24933642)

    def test_y2022d08(self):
        assert get_day_result(self.year, 8) == (21, 8)

    def test_y2022d09(self):
        assert get_day_result(self.year, 9) == (13, 1)

    def test_y2022d10(self):
        result2 = (
                '##..##..##..##..##..##..##..##..##..##..\n'
                '###...###...###...###...###...###...###.\n'
                '####....####....####....####....####....\n'
                '#####.....#####.....#####.....#####.....\n'
                '######......######......######......####\n'
                '#######.......#######.......#######.....'
                )
        assert get_day_result(self.year, 10) == (13140, result2)

    def test_y2022d11(self):
        assert get_day_result(self.year, 11) == (10605, 2713310158)

    def test_y2022d12(self):
        assert get_day_result(self.year, 12) == (31, 29)

    def test_y2022d13(self):
        assert get_day_result(self.year, 13) == (13, 140)

    def test_y2022d14(self):
        assert get_day_result(self.year, 14) == (24, 93)

    def test_y2022d15(self):
        assert get_day_result(self.year, 15) == (26, 56000011)

    def test_y2022d16(self):
        assert get_day_result(self.year, 16) == (1651, 1707)

    def test_y2022d17(self):
        assert get_day_result(self.year, 17) == (3068, 1514285714288)

    def test_y2022d18(self):
        assert get_day_result(self.year, 18) == (64, 58)

    def test_y2022d19(self):
        assert get_day_result(self.year, 19) == (33, 0)

    def test_y2022d20(self):
        assert get_day_result(self.year, 20) == (3, 1623178306)

    def test_y2022d21(self):
        assert get_day_result(self.year, 21) == (152, 301)

    def test_y2022d22(self):
        assert get_day_result(self.year, 22) == (6032, 5031)

    def test_y2022d23(self):
        assert get_day_result(self.year, 23) == (110, 20)

    def test_y2022d24(self):
        assert get_day_result(self.year, 24) == (18, 54)

    def test_y2022d25(self):
        from y2022.d25 import encode_snafu
        assert encode_snafu(1) == '1'
        assert encode_snafu(2) == '2'
        assert encode_snafu(3) == '1='
        assert encode_snafu(4) == '1-'
        assert encode_snafu(5) == '10'
        assert encode_snafu(6) == '11'
        assert encode_snafu(7) == '12'
        assert encode_snafu(8) == '2='
        assert encode_snafu(9) == '2-'
        assert encode_snafu(10) == '20'
        assert get_day_result(self.year, 25) == ('2=-1=0', 0)
