"""Advent of Code 2022

Day 13: Distress Signal

https://adventofcode.com/2022/day/13
"""
import logging  # noqa: F401
import json
from functools import cmp_to_key

from util import timing


def compare(a, b) -> int:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0
    elif isinstance(a, list) and isinstance(b, list):
        for i in range(len(a)):
            if i >= len(b):
                return 1
            result = compare(a[i], b[i])
            if result != 0:
                return result
        if len(a) < len(b):
            return -1
        return 0
    elif isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])
    else:
        return compare([a], b)


def parse(stream) -> str:
    text = stream.read()
    blocks = text.split('\n\n')
    result = []
    for block in blocks:
        a, b = block.strip().split('\n')
        a = json.loads(a)
        b = json.loads(b)
        result.append((a, b))
    return result


def get_valid_pairs(pairs):
    result = []
    for i, (a, b) in enumerate(pairs):
        if compare(a, b) < 0:
            result.append(i + 1)
    return result


def get_decoder_key(pairs):
    diva = [[2]]
    divb = [[6]]

    packets = []
    for pair in pairs:
        packets.extend(pair)
    packets.append(diva)
    packets.append(divb)
    packets.sort(key=cmp_to_key(compare))

    return (packets.index(diva) + 1) * (packets.index(divb) + 1)


def run(stream, test: bool = False):
    with timing("Part 1"):
        pairs = parse(stream)
        valid = get_valid_pairs(pairs)
        result1 = sum(valid)

    with timing("Part 2"):
        result2 = get_decoder_key(pairs)

    return (result1, result2)
