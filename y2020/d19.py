"""Advent of Code 2020

Day 19: Monster Messages

https://adventofcode.com/2020/day/19
"""
import logging  # noqa: F401
import re
from collections import defaultdict, deque

from util import timing


class Tree:
    def __init__(self, stream=''):
        self.nodes = dict
        self.messages = []
        self.rule2 = False

        if stream:
            self.parse(stream)

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')

        nodes = defaultdict(list)
        for line in stream:
            line = line.strip()
            if line == '':
                break
            head, prods = line.split(': ')
            head = int(head)
            prods = prods.split(' | ')
            for prod in prods:
                if prod.startswith('"') and prod.endswith('"'):
                    rules = prod[1:-1]
                else:
                    rules = tuple(int(x) for x in prod.split(' '))
                nodes[head].append(rules)
        self.nodes = dict(nodes)

        for line in stream:
            line = line.strip()
            if line == '':
                continue
            self.messages.append(line)

    def to_regex(self, start: int = 0) -> re.Pattern:
        expr = [start]
        q = deque([start])
        while q:
            node = q.popleft()
            prods = self.nodes.get(node, [])
            if self.rule2 and node == 8:
                repl = (42, '+')
            elif self.rule2 and node == 11:
                repl = (42, '+', 31, '+')
            elif len(prods) > 1:
                repl = ['(']
                for prod in prods[:-1]:
                    repl.extend(prod)
                    repl.append('|')
                repl.extend(prods[-1])
                repl.append(')')
            else:
                repl = prods[0]

            rules = {x for x in repl if isinstance(x, int)}
            q.extend(rules)

            newexpr = []
            for i in range(len(expr)):
                value = expr[i]
                if value == node:
                    newexpr.extend(repl)
                else:
                    newexpr.append(value)
            expr = newexpr
        # All replacements complete, all elements of `expr` should be str now,
        # render it to a compiled regex Pattern.
        text = ''.join(expr)
        return re.compile(text)

    def count_valid_messages(self) -> int:
        regex = self.to_regex()
        result = 0
        for message in self.messages:
            if regex.fullmatch(message):
                result += 1
        return result


def parse(stream) -> Tree:
    return Tree(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        tree = parse(stream)
        result1 = tree.count_valid_messages()

    with timing("Part 2"):
        tree.rule2 = True
        result2 = tree.count_valid_messages()

    return (result1, result2)
