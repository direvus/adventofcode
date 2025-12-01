"""Advent of Code 2025

Day 1: Secret Entrance

https://adventofcode.com/2025/day/1
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        n = int(line[1:])
        if line[0] == 'L':
            n = -n
        result.append(n)
    return result


def count_zeroes(moves):
    result = 0
    pos = 50
    for move in moves:
        pos = (pos + move) % 100
        if pos == 0:
            result += 1
    return result


def count_zero_clicks(moves):
    result = 0
    pos = 50
    for move in moves:
        step = 1 if move > 0 else -1
        for _ in range(abs(move)):
            pos = (pos + step) % 100
            if pos == 0:
                result += 1
    return result

def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = tuple(parse(stream))
        result1 = count_zeroes(parsed)

    with timing("Part 2"):
        result2 = count_zero_clicks(parsed)

    return (result1, result2)
