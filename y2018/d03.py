"""Advent of Code 2018

Day 3: No Matter How You Slice It

https://adventofcode.com/2018/day/3
"""
import logging  # noqa: F401
from collections import namedtuple, Counter
from itertools import combinations

from util import timing


Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])


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


def get_all_cells(claims: tuple) -> set:
    result = set()
    for claim in claims:
        for y in range(claim.top, claim.top + claim.height):
            for x in range(claim.left, claim.left + claim.width):
                result.add((y, x))
    return result


def in_claim(claim, cell):
    y, x = cell
    return (y >= claim.top and y < claim.top + claim.height and
            x >= claim.left and x < claim.left + claim.width)


def count_overlapped_cells(claims: tuple) -> int:
    result = 0
    cells = get_all_cells(claims)
    for cell in cells:
        count = 0
        for claim in claims:
            count += int(in_claim(claim, cell))
            if count >= 2:
                result += 1
                break
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        claims = parse(stream)
        result1 = count_overlapped_cells(claims)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
