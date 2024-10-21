"""Advent of Code 2020

Day 16: Ticket Translation

https://adventofcode.com/2020/day/16
"""
import logging  # noqa: F401
from math import prod

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

    def discard_tickets(self, numbers: set[int]):
        tickets = tuple(self.others)
        for ticket in tickets:
            if any(n in ticket for n in numbers):
                self.others.discard(ticket)

    def find_field_positions(self):
        count = len(self.fields)
        fields = set(self.fields.keys())
        positions = set(range(count))
        tickets = (self.ticket,) + tuple(self.others)
        result = {}
        while fields:
            for i in range(count):
                if i not in positions:
                    continue
                candidates = set(fields)
                for ticket in tickets:
                    value = ticket[i]
                    candidates &= {
                            f for f in fields
                            if self.fields[f].contains(value)}
                if len(candidates) == 1:
                    field = next(iter(candidates))
                    result[field] = i
                    fields.discard(field)
                    positions.discard(i)
        return result

    def get_departure_values(self, positions: dict):
        return {
                self.ticket[i] for k, i in positions.items()
                if k.startswith('departure')}


def parse(stream) -> Tickets:
    return Tickets(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        tickets = parse(stream)
        invalid = tickets.find_invalid_numbers()
        result1 = sum(invalid)

    with timing("Part 2"):
        tickets.discard_tickets(invalid)
        positions = tickets.find_field_positions()
        values = tickets.get_departure_values(positions)
        result2 = prod(values)

    return (result1, result2)
