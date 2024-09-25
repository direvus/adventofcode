"""Advent of Code 2018

Day 3: No Matter How You Slice It

https://adventofcode.com/2018/day/3
"""
import logging  # noqa: F401
from itertools import combinations

from util import timing


class Claim:
    number: int
    left: int
    top: int
    width: int
    height: int

    def __init__(self, number, left, top, width, height):
        self.number = number
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    @property
    def bottom(self) -> int:
        return self.top + self.height - 1

    @property
    def right(self) -> int:
        return self.left + self.width - 1

    @property
    def cells(self) -> set:
        result = set()
        for y in range(self.top, self.bottom + 1):
            for x in range(self.left, self.right + 1):
                result.add((y, x))
        return result

    def is_disjoint(self, other) -> bool:
        return (self.right < other.left or other.right < self.left or
                self.bottom < other.top or other.bottom < self.top)

    def union(self, other) -> 'Claim':
        if self.is_disjoint(other):
            return Claim(0, 0, 0, 0, 0)

        left = max(self.left, other.left)
        top = max(self.top, other.top)
        right = min(self.right, other.right)
        bottom = min(self.bottom, other.bottom)

        width = right - left + 1
        height = bottom - top + 1
        return Claim(0, left, top, width, height)

    def contains_cell(self, cell) -> bool:
        y, x = cell
        return (y >= self.top and y < self.top + self.height and
                x >= self.left and x < self.left + self.width)


def parse(stream) -> tuple:
    result = []
    for line in stream:
        line = line.strip()
        i, rest = line[1:].split(' @ ')
        corner, size = rest.split(': ')
        left, top = (int(x) for x in corner.split(','))
        width, height = (int(x) for x in size.split('x'))

        result.append(Claim(int(i), left, top, width, height))
    return tuple(result)


def count_overlapped_cells(claims: tuple) -> int:
    cells = set()
    for a, b in combinations(claims, 2):
        cells |= a.union(b).cells
    return len(cells)


def has_overlaps(claim: Claim, others: tuple) -> bool:
    for other in others:
        if other.number != claim.number and not claim.is_disjoint(other):
            return True
    return False


def get_nonoverlapping_claim(claims: tuple) -> Claim | None:
    for claim in claims:
        if not has_overlaps(claim, claims):
            return claim


def run(stream, test: bool = False):
    with timing("Part 1"):
        claims = parse(stream)
        result1 = count_overlapped_cells(claims)

    with timing("Part 2"):
        nonoverlap = get_nonoverlapping_claim(claims)
        result2 = nonoverlap.number if nonoverlap else None

    return (result1, result2)
