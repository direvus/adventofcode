"""Advent of Code 2020

Day 2: Password Philosophy

https://adventofcode.com/2020/day/2
"""
import logging  # noqa: F401
from collections import namedtuple, Counter

from util import timing


Entry = namedtuple('Entry', ('min', 'max', 'letter', 'password'))


def parse(stream) -> tuple[Entry]:
    result = []
    for line in stream:
        policy, password = line.strip().split(': ')
        nums, letter = policy.split(' ')
        minc, maxc = (int(x) for x in nums.split('-'))
        entry = Entry(minc, maxc, letter, password)
        result.append(entry)
    return tuple(result)


def is_valid(entry: Entry) -> bool:
    counts = Counter(entry.password)
    count = counts[entry.letter]
    return count >= entry.min and count <= entry.max


def is_valid2(entry: Entry) -> bool:
    letter1 = entry.password[entry.min - 1]
    letter2 = entry.password[entry.max - 1]
    return (entry.letter == letter1) != (entry.letter == letter2)


def count_valid(entries: tuple[Entry]) -> int:
    return sum(int(is_valid(e)) for e in entries)


def count_valid2(entries: tuple[Entry]) -> int:
    return sum(int(is_valid2(e)) for e in entries)


def run(stream, test: bool = False):
    with timing("Part 1"):
        entries = parse(stream)
        result1 = count_valid(entries)

    with timing("Part 2"):
        result2 = count_valid2(entries)

    return (result1, result2)
