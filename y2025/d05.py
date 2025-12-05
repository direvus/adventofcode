"""Advent of Code 2025

Day 5: Cafeteria

https://adventofcode.com/2025/day/5
"""
import logging  # noqa: F401

from util import timing
from spans import SpanSet


def parse(stream) -> str:
    spans = SpanSet()
    ingreds = set()
    for line in stream:
        line = line.strip()
        if line == '':
            break
        a, b = map(int, line.split('-'))
        spans.add_span((a, b))

    for line in stream:
        ingreds.add(int(line))

    return spans, ingreds


def run(stream, test: bool = False):
    with timing("Part 1"):
        spans, ingreds = parse(stream)
        result1 = sum([spans.contains(x) for x in ingreds])

    with timing("Part 2"):
        result2 = spans.total

    return (result1, result2)
