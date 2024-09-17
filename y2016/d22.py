"""Advent of Code 2016

Day 22: Grid Computing

https://adventofcode.com/2016/day/22
"""
import logging  # noqa: F401
import re
from collections import namedtuple
from itertools import permutations

from util import timing


PATTERN = re.compile(r'node-x(\d+)-y(\d+)')
Node = namedtuple('node', ['x', 'y', 'size', 'used', 'avail', 'usep'])


def parse(stream) -> dict:
    result = {}
    for line in stream:
        words = line.strip().split()
        m = PATTERN.search(words[0])
        if not m:
            # Skip header lines
            continue
        x, y = m.groups()

        # All the sizes are given in T, so ignore the units
        size = int(words[1][:-1])
        used = int(words[2][:-1])
        avail = int(words[3][:-1])
        usep = int(words[4][:-1])

        node = Node(x, y, size, used, avail, usep)
        result[(x, y)] = node
    return result


def get_viable_pairs(nodes: dict) -> tuple:
    result = []
    for a, b in permutations(nodes.values(), 2):
        if a.used > 0 and a.used <= b.avail:
            result.append(((a.x, a.y), (b.x, b.y)))
    return result


def run(stream, test: bool = False):
    nodes = parse(stream)
    logging.debug(f"Parsed {len(nodes)} nodes")

    with timing("Part 1"):
        result1 = len(get_viable_pairs(nodes))
    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
