"""Advent of Code 2020

Day 24: Lobby Layout

https://adventofcode.com/2020/day/24
"""
import logging  # noqa: F401

from util import timing


# This hex grid uses a pointy-top orientation, with a 2D coordinate system
# where the first axis is in the SE direction, and the second axis is in the NE
# direction.


VECTORS = {
        'se': (1, 0),
        'ne': (0, 1),
        'e':  (1, 1),
        'nw': (-1, 0),
        'sw': (0, -1),
        'w':  (-1, -1),
        }


def get_distance(a: tuple, b: tuple) -> int:
    return max(abs(b[0] - a[0]), abs(b[1] - a[1]))


def move(position: tuple, direction: str) -> tuple:
    se, ne = position
    vse, vne = VECTORS[direction]
    return (se + vse, ne + vne)


class Grid:
    def __init__(self):
        self.flipped = set()

    def flip(self, position: tuple):
        if position in self.flipped:
            self.flipped.remove(position)
        else:
            self.flipped.add(position)


def parse_line(line: str) -> tuple:
    p = (0, 0)
    i = 0
    while i < len(line):
        if line[i] in 'ew':
            p = move(p, line[i])
            i += 1
        else:
            p = move(p, line[i:i + 2])
            i += 2
    return p


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        pos = parse_line(line)
        result.append(pos)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        positions = parse(stream)
        grid = Grid()
        for pos in positions:
            grid.flip(pos)
        result1 = len(grid.flipped)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
