"""Advent of Code 2021

Day 6: Lanternfish

https://adventofcode.com/2021/day/6
"""
import logging  # noqa: F401
from collections import Counter

from util import timing


def parse(stream) -> Counter:
    line = stream.readline().strip()
    return Counter((int(x) for x in line.split(',')))


def do_round(counts: Counter) -> Counter:
    result = Counter()
    for timer, count in counts.items():
        if timer > 0:
            result[timer - 1] += count
        else:
            result[8] += count
            result[6] += count
    return result


def simulate(counts: Counter, rounds: int = 1) -> Counter:
    for _ in range(rounds):
        counts = do_round(counts)
    return counts


def run(stream, test: bool = False):
    with timing("Part 1"):
        initial = parse(stream)
        counts = simulate(initial, 80)
        result1 = counts.total()

    with timing("Part 2"):
        counts = simulate(initial, 256)
        result2 = counts.total()

    return (result1, result2)
