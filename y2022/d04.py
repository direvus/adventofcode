"""Advent of Code 2022

Day 4: Camp Cleanup

https://adventofcode.com/2022/day/4
"""
import logging  # noqa: F401

from util import timing
from spans import span_contains, span_overlaps


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        spans = line.split(',')
        spans = tuple(
                tuple(int(x) for x in span.split('-'))
                for span in spans)
        result.append(spans)
    return result


def count_relations(pairs) -> tuple:
    contains = 0
    overlaps = 0
    for a, b in pairs:
        if span_contains(a, b) or span_contains(b, a):
            contains += 1
            overlaps += 1
        elif span_overlaps(a, b):
            overlaps += 1
    return contains, overlaps


def run(stream, test: bool = False):
    with timing("Both Parts"):
        parsed = parse(stream)
        result1, result2 = count_relations(parsed)

    return (result1, result2)
