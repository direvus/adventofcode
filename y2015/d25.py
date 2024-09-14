import re
from functools import cache


KNOWN = {
        0: 20151125,
        1: 31916031,
        2: 18749137,
        3: 16080970,
        4: 21629792,
        5: 17289845,
        6: 24592653,
        7: 8057251,
        8: 16929656,
        9: 30943339,
        10: 77061,
        11: 32451966,
        12: 1601130,
        13: 7726640,
        14: 10071777,
        15: 33071741,
        16: 17552253,
        17: 21345942,
        18: 7981243,
        19: 15514188,
        20: 33511524,
        22: 6796745,
        23: 28094349,
        24: 9380097,
        25: 11661866,
        26: 4041754,
        30: 25397450,
        31: 6899651,
        32: 10600672,
        33: 16474243,
        39: 24659492,
        40: 9250759,
        41: 31527494,
        49: 1534922,
        50: 31663883,
        60: 27995004,
        }


def parse(stream) -> set:
    pat = re.compile(r'row (\d+), column (\d+)')
    line = stream.readline().strip()
    m = pat.search(line)
    row, col = m.groups()
    return int(row), int(col)


def get_index(row: int, col: int) -> int:
    """Translate a row and column position into a 1-D index."""
    i = col - 1
    base = row + i - 1
    return (base ** 2 + base) / 2 + i


@cache
def get_next_cell(value: int) -> int:
    return (value * 252533) % 33554393


def get_value_at_cell(row: int, col: int) -> int:
    index = get_index(row, col)
    if index in KNOWN:
        return KNOWN[index]
    options = [k for k in KNOWN.keys() if k < index]
    last = max(options)
    i = last
    value = KNOWN[last]
    while i < index:
        value = get_next_cell(value)
        i += 1
    return value


def run(stream, test=False, draw=False):
    row, col = parse(stream)

    result1 = get_value_at_cell(row, col)
    result2 = 0

    return (result1, result2)
