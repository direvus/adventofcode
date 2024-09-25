"""Advent of Code 2018

Day 2: Inventory Management System

https://adventofcode.com/2018/day/2
"""
import logging  # noqa: F401
from collections import Counter
from itertools import combinations

from util import timing


def parse(stream) -> tuple:
    result = []
    for line in stream:
        result.append(line.strip())
    return tuple(result)


def get_checksum(boxes: tuple) -> int:
    groups = Counter()
    for box in boxes:
        letters = Counter(box)
        values = set(letters.values())
        for v in values:
            groups[v] += 1
    return groups[2] * groups[3]


def find_box_id(boxes: tuple) -> str | None:
    for a, b in combinations(boxes, 2):
        common = tuple(x for i, x in enumerate(a) if b[i] == x)
        if len(common) == len(a) - 1:
            return ''.join(common)


def run(stream, test: bool = False):
    with timing("Part 1"):
        boxes = parse(stream)
        result1 = get_checksum(boxes)

    with timing("Part 2"):
        result2 = find_box_id(boxes)

    return (result1, result2)
