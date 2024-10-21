"""Advent of Code 2020

Day 16: Ticket Translation

https://adventofcode.com/2020/day/16
"""
import logging  # noqa: F401

from spans import SpanSet
from util import timing


class Tickets:
    def __init__(self, stream=''):
        self.fields = {}
        self.ticket = None
        self.others = set()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        # Blocks are separated by a blank line.
        # First block is the fields
        for line in stream:
            line = line.strip()
            if line == '':
                break
            name, ranges = line.split(': ')
            ranges = ranges.split(' or ')
            spans = SpanSet()
            for r in ranges:
                low, high = r.split('-')
                spans.add_span((int(low), int(high)))
            self.fields[name] = spans

        # Skip the 'your ticket:' header line
        stream.readline()
        line = stream.readline().strip()
        self.ticket = tuple(int(x) for x in line.split(','))

        # Skip the blank line and the 'nearby tickets:' header line
        stream.readline()
        stream.readline()
        for line in stream:
            line = line.strip()
            ticket = tuple(int(x) for x in line.split(','))
            self.others.add(ticket)

    def is_valid(self, value: int) -> bool:
        for spans in self.fields.values():
            if spans.contains(value):
                return True
        return False

    def find_invalid_numbers(self) -> list[int]:
        result = []
        for ticket in self.others:
            for n in ticket:
                if not self.is_valid(n):
                    result.append(n)
        return result


def parse(stream) -> Tickets:
    return Tickets(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        tickets = parse(stream)
        result1 = sum(tickets.find_invalid_numbers())

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
