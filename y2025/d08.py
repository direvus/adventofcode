"""Advent of Code 2025

Day 8: Playground

https://adventofcode.com/2025/day/8
"""
import logging  # noqa: F401
from itertools import combinations
from functools import reduce
from operator import mul

from util import get_euclidean_distance, timing


def parse(stream) -> str:
    return [
            tuple(map(int, x.strip().split(',')))
            for x in stream]


def make_circuits(boxes, count):
    """Make circuits by connecting the `count` closest-together boxes.
    """
    distances = [(a, b, get_euclidean_distance(a, b))
                 for a, b in combinations(boxes, 2)]
    # Sort in reverse order so we can pop elements off the end.
    distances.sort(key=lambda x: x[2], reverse=True)

    # Initially put each box into its own circuit
    circuits = []
    index = {}
    for i, x in enumerate(boxes):
        circuits.append({x})
        index[x] = i

    i = 0
    while i < count:
        a, b, _ = distances.pop()
        ca = index[a]
        cb = index[b]
        if ca == cb:
            # Already in the same circuit, do nothing
            i += 1
            continue
        # Merge the circuit of B into the circuit of A
        circuits[ca] |= circuits[cb]
        for box in circuits[cb]:
            index[box] = ca
        circuits[cb] = set()
        i += 1

    return circuits


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        count = 10 if test else 1000
        circuits = make_circuits(set(parsed), count)
        sizes = sorted(map(len, circuits), reverse=True)
        top = sizes[:3]
        result1 = reduce(mul, top, 1)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
