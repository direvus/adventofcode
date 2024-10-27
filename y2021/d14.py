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


class Extender:
    def __init__(self, rules: dict):
        self.rules = dict(rules)
        self.cache = {}

        for pair, insert in rules.items():
            self.cache[pair] = {1: Counter(insert)}

    def count_inserts(self, node: str, levels: int) -> Counter:
        cached = self.cache.get(node, {}).get(levels)
        if cached:
            return cached

        insert = self.rules[node]
        counter = Counter(insert)

        left = node[0] + insert
        right = insert + node[1]
        counter.update(self.count_inserts(left, levels - 1))
        counter.update(self.count_inserts(right, levels - 1))

        self.cache[node][levels] = counter
        return counter


def do_updates(template: str, extender: Extender, count: int) -> Counter:
    counter = Counter(template)
    for i in range(len(template) - 1):
        node = template[i:i + 2]
        counter.update(extender.count_inserts(node, count))
    return counter


def get_score(counter: Counter) -> int:
    items = [v for v in counter.values()]
    items.sort()
    least = items[0]
    most = items[-1]
    return most - least


def run(stream, test: bool = False):
    with timing("Part 1"):
        template, rules = parse(stream)
        extender = Extender(rules)
        counter = do_updates(template, extender, 10)
        result1 = get_score(counter)

    with timing("Part 2"):
        counter = do_updates(template, extender, 40)
        result2 = get_score(counter)

    return (result1, result2)
