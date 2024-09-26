"""Advent of Code 2018

Day 5: Alchemical Reduction

https://adventofcode.com/2018/day/5
"""
import logging  # noqa: F401
import string

from util import timing, INF


def parse(stream) -> str:
    return stream.readline().strip()


def is_reactive(a: str, b: str) -> bool:
    return a.upper() == b.upper() and a != b


def reduce(value: str) -> str:
    result = []
    count = len(value) - 1
    i = 0
    while i < count:
        ch = value[i]
        if is_reactive(ch, value[i + 1]):
            i += 2
            while result and i <= count and is_reactive(result[-1], value[i]):
                result.pop()
                i += 1
        else:
            result.append(ch)
            i += 1

    if i <= count:
        result.append(value[i])
    return ''.join(result)


def find_shortest(value: str) -> int:
    best = INF
    for letter in string.ascii_lowercase:
        v = value.replace(letter, '').replace(letter.upper(), '')
        length = len(reduce(v))
        logging.debug(f"Removing {letter} yields {length}")
        if length < best:
            best = length
    return best


def run(stream, test: bool = False):
    with timing("Part 1"):
        value = parse(stream)
        reduced = reduce(value)
        result1 = len(reduced)

    with timing("Part 2"):
        result2 = find_shortest(value)

    return (result1, result2)
