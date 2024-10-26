"""Advent of Code 2021

Day 14: Extended Polymerization

https://adventofcode.com/2021/day/14
"""
import logging  # noqa: F401
from collections import Counter

from util import timing


def parse(stream) -> tuple[str, dict]:
    rules = {}
    template = stream.readline().strip()
    # Skip one blank line
    stream.readline()

    for line in stream:
        line = line.strip()
        pair, insert = line.split(' -> ')
        rules[pair] = insert
    return template, rules


def update(polymer: str, rules: dict) -> str:
    result = []
    for i in range(1, len(polymer)):
        chunk = polymer[i - 1: i + 1]
        result.append(chunk[0])
        if chunk in rules:
            result.append(rules[chunk])
    result.append(polymer[-1])
    return ''.join(result)


def do_updates(template: str, rules: dict, count: int) -> str:
    value = template
    for i in range(count):
        value = update(value, rules)
    return value


def get_score(polymer: str) -> int:
    counter = Counter(polymer)
    items = [v for v in counter.values()]
    items.sort()
    least = items[0]
    most = items[-1]
    return most - least


def run(stream, test: bool = False):
    with timing("Part 1"):
        template, rules = parse(stream)
        value = do_updates(template, rules, 10)
        result1 = get_score(value)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
