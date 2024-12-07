"""Advent of Code 2024

Day 1: Historian Hysteria

https://adventofcode.com/2024/day/1
"""
import logging  # noqa: F401
from collections import Counter

from util import timing


def parse(stream) -> str:
    left = []
    right = []
    for line in stream:
        line = line.strip()
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    return left, right


def get_total_distances(left, right):
    left.sort()
    right.sort()

    pairs = zip(left, right)
    return sum(abs(a - b) for a, b in pairs)


def get_similarity_score(left, right):
    counter = Counter(right)
    result = 0
    for value in left:
        result += value * counter[value]
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        left, right = parse(stream)
        result1 = get_total_distances(left, right)

    with timing("Part 2"):
        result2 = get_similarity_score(left, right)

    return (result1, result2)