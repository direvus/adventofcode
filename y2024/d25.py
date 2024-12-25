"""Advent of Code 2024

Day 25: Code Chronicle

https://adventofcode.com/2024/day/25
"""
import logging  # noqa: F401

from util import timing


SIZE = 5


def parse_block(stream):
    line = stream.readline().strip()
    if line == '':
        return None
    result = [None] * (len(line) + 1)
    lock = line.startswith('#')
    blank = '.' if lock else '#'
    result[0] = lock

    i = 0
    for line in stream:
        line = line.strip()
        if line == '':
            break
        for j, ch in enumerate(line):
            if result[j + 1] is None and ch == blank:
                height = i if lock else SIZE - i
                result[j + 1] = height
        i += 1
    return result

def parse(stream) -> str:
    locks = []
    keys = []
    block = parse_block(stream)
    while block is not None:
        lock = block[0]
        heights = block[1:]
        if lock:
            locks.append(heights)
        else:
            keys.append(heights)
        block = parse_block(stream)
    return locks, keys


def is_compatible(lock, key):
    for a, b in zip(lock, key):
        if (a + b) > SIZE:
            return False
    return True


def get_compatible_pairs(locks, keys):
    result = []
    for lock in locks:
        for key in keys:
            if is_compatible(lock, key):
                result.append((lock, key))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        locks, keys = parse(stream)
        result1 = len(get_compatible_pairs(locks, keys))

    return (result1, 0)
