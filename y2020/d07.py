"""Advent of Code 2020

Day 7: Handy Haversacks

https://adventofcode.com/2020/day/7
"""
import logging  # noqa: F401
import re
from collections import defaultdict

from util import timing


PARSER = re.compile(r'^(\w+ \w+) bags contain (.+)\.$')


class Graph:
    def __init__(self, stream):
        self.nodes = set()
        self.children = defaultdict(dict)
        self.parents = defaultdict(set)

        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PARSER.fullmatch(line)
            if not m:
                continue
            container, contents = m.groups()
            self.nodes.add(container)
            if contents == 'no other bags':
                continue
            for content in contents.split(', '):
                words = content.split()
                count = int(words[0])
                bagtype = f'{words[1]} {words[2]}'
                self.children[container][bagtype] = count
                self.parents[bagtype].add(container)

    def count_containments(self, bagtype: str) -> int:
        """Count the number of bag that can contain `bagtype`.

        This is the number of distinct bags that are in any path from `bagtype`
        up to any top-level node.
        """
        types = set()
        q = [x for x in self.parents[bagtype]]
        while q:
            node = q.pop(0)
            types.add(node)

            for parent in self.parents[node]:
                q.append(parent)
        return len(types)

    def count_contained(self, bagtype: str) -> int:
        """Count all the bags that are contained in `bagtype`."""
        result = 0
        q = [(bagtype, 1)]
        while q:
            node, count = q.pop(0)
            for child, num in self.children[node].items():
                total = count * num
                result += total
                q.append((child, total))
        return result


def parse(stream) -> Graph:
    return Graph(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        g = parse(stream)
        result1 = g.count_containments('shiny gold')

    with timing("Part 2"):
        result2 = g.count_contained('shiny gold')

    return (result1, result2)
