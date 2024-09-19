"""Advent of Code 2017

Day 3: Spiral Memory

https://adventofcode.com/2017/day/3
"""
import logging


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


def find_cumulative(target: int) -> int:
    i = 0
    loops = 1
    side = loops * 2
    length = side * 4
    values = {(0, 0): 1}
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # Up, Left, Down, Right
    d = 0
    pos = (0, 1)
    n = 1
    while n <= target:
        y, x = pos
        neighbours = (
                (y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1),
                (y - 1, x - 1), (y - 1, x + 1), (y + 1, x - 1), (y + 1, x + 1),
                )
        n = sum(values.get(x, 0) for x in neighbours)
        logging.debug(f"At {pos}, n = {n}")
        values[pos] = n
        i += 1
        if i == length:
            # Start a new loop
            pos = (y, x + 1)
            d = 0
            i = 0
            loops += 1
            side = loops * 2
            length = side * 4
            logging.debug(f"Starting next loop at {pos}")
            continue
        if i % side == 0:
            # Turn a corner
            d = (d + 1) % 4
            logging.debug(f"Turning to face {directions[d]}")
        dy, dx = directions[d]
        pos = (y + dy, x + dx)
        logging.debug(f"Next position is {pos}")
    return n


def run(stream, test=False):
    target = parse(stream)
    result1 = find_distance(target)
    result2 = find_cumulative(target)

    return (result1, result2)
