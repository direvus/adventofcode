import unittest

from tests.common import get_day_result


class TestSolutions2021(unittest.TestCase):
    year = 2021

    def test_y2021d01(self):
        assert get_day_result(self.year, 1) == (7, 5)

    def test_y2021d02(self):
        assert get_day_result(self.year, 2) == (150, 900)

    def test_y2021d03(self):
        assert get_day_result(self.year, 3) == (198, 230)

    def test_y2021d04(self):
        assert get_day_result(self.year, 4) == (4512, 1924)

    def test_y2021d05(self):
        assert get_day_result(self.year, 5) == (5, 12)

    def test_y2021d06(self):
        assert get_day_result(self.year, 6) == (5934, 26984457539)

    def test_y2021d07(self):
        assert get_day_result(self.year, 7) == (37, 168)

    def test_y2021d08(self):
        assert get_day_result(self.year, 8) == (26, 61229)

    def test_y2021d09(self):
        assert get_day_result(self.year, 9) == (15, 1134)

    def test_y2021d10(self):
        assert get_day_result(self.year, 10) == (26397, 288957)

    def test_y2021d11(self):
        assert get_day_result(self.year, 11) == (1656, 195)

    def test_y2021d12(self):
        assert get_day_result(self.year, 12) == (10, 36)

    def test_y2021d13(self):
        assert get_day_result(self.year, 13) == (
                17,
                '#####\n'
                '#...#\n'
                '#...#\n'
                '#...#\n'
                '#####')

    def test_y2021d14(self):
        assert get_day_result(self.year, 14) == (1588, 2188189693529)

    def test_y2021d15(self):
        assert get_day_result(self.year, 15) == (40, 315)

    def test_y2021d16(self):
        from y2021.d16 import Message

        m = Message('38006F45291200')
        p = m.decode_packet()
        assert p.version == 1
        assert p.typeid == 6
        assert len(p.packets) == 2
        assert p.packets[0].value == 10
        assert p.packets[1].value == 20

        m = Message('EE00D40C823060')
        p = m.decode_packet()
        assert p.version == 7
        assert p.typeid == 3
        assert len(p.packets) == 3
        assert p.packets[0].value == 1
        assert p.packets[1].value == 2
        assert p.packets[2].value == 3

        m = Message('8A004A801A8002F478')
        p = m.decode_packet()
        assert p.get_total_versions() == 16

        m = Message('620080001611562C8802118E34')
        p = m.decode_packet()
        assert p.get_total_versions() == 12

        m = Message('C0015000016115A2E0802F182340')
        p = m.decode_packet()
        assert p.get_total_versions() == 23

        m = Message('A0016C880162017C3686B18A3D4780')
        p = m.decode_packet()
        assert p.get_total_versions() == 31

        assert get_day_result(self.year, 16) == (6, 2021)

    def test_y2021d17(self):
        assert get_day_result(self.year, 17) == (45, 112)

    def test_y2021d18(self):
        assert get_day_result(self.year, 18) == (4140, 3993)

    def test_y2021d19(self):
        assert get_day_result(self.year, 19) == (79, 3621)

    def test_y2021d20(self):
        assert get_day_result(self.year, 20) == (35, 3351)

    def test_y2021d21(self):
        assert get_day_result(self.year, 21) == (739785, 7907)

    def test_y2021d22(self):
        from y2021.d22 import (
                disjoint, contains, divide,
                get_total_volume, get_volume, Grid)
        grid = Grid()
        a = (10, 12, 10, 12, 10, 12)
        b = (11, 13, 11, 13, 11, 13)
        assert get_volume(a) == 27
        assert disjoint(a, b) is False
        assert contains(a, b) is False
        assert contains(b, a) is False
        div = divide(a, b)
        assert get_total_volume(div) == 27
        grid.activate(a)
        assert grid.total_active == 27
        grid.activate(b)
        assert grid.total_active == 27 + 19

        assert get_day_result(self.year, 22) == (590784, 39769202357779)

    def test_y2021d23(self):
        assert get_day_result(self.year, 23) == (12521, 44169)

    def test_y2021d24(self):
        assert get_day_result(self.year, 24) == ([0, 1, 1, 1], 0)

    def test_y2021d25(self):
        assert get_day_result(self.year, 25) == (58, None)
