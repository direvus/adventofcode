"""Advent of Code 2017

Day 3: Spiral Memory

https://adventofcode.com/2017/day/3
"""


def parse(stream) -> int:
    return int(stream.readline().strip())


def find_distance(number: int) -> int:
    """Return the distance of `number` from the central point."""
    if number == 1:
        return 0
    i = 1
    corner = 1
    side = i * 2
    length = side * 4
    while corner + length < number:
        corner += length
        i += 1
        side = i * 2
        length = side * 4
    diff = number - corner
    mod = diff % side
    if mod == 0:
        # Literally a corner case
        return i * 2
    return i + abs(mod - side // 2)


def run(stream, test=False):
    target = parse(stream)
    result1 = find_distance(target)
    result2 = 0

    return (result1, result2)
