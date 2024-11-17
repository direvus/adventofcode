"""Advent of Code 2022

Day 3: Rucksack Reorganization

https://adventofcode.com/2022/day/3
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list:
    items = []
    for line in stream:
        line = line.strip()
        half = len(line) // 2
        items.append((line[:half], line[half:]))
    return items


def get_priority(item: str) -> int:
    code = ord(item)
    if code < 97:
        # Uppercase: A == 27
        return code - 65 + 27
    else:
        # Lowercase: a == 1
        return code - 96


def get_total_priority(items) -> int:
    result = 0
    for a, b in items:
        common = set(a) & set(b)
        assert len(common) == 1
        item = next(iter(common))
        result += get_priority(item)
    return result


def get_total_badge_priority(items) -> int:
    i = 0
    result = 0
    for i in range(0, len(items), 3):
        unions = tuple(set(a) | set(b) for a, b in items[i: i + 3])
        common = unions[0] & unions[1] & unions[2]
        assert len(common) == 1
        item = next(iter(common))
        result += get_priority(item)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_total_priority(parsed)

    with timing("Part 2"):
        result2 = get_total_badge_priority(parsed)

    return (result1, result2)
