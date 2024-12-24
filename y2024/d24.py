"""Advent of Code 2024

Day 24: Crossed Wires

https://adventofcode.com/2024/day/24
"""
import logging  # noqa: F401
from collections import deque
from operator import and_, or_, xor

from util import timing


def parse(stream) -> str:
    wires = []
    gates = []
    for line in stream:
        line = line.strip()
        if line == '':
            break
        wire, value = line.split(': ')
        value = int(value)
        wires.append((wire, value))

    for line in stream:
        line = line.strip()
        expr, out = line.split(' -> ')
        a, op, b = expr.split()
        gates.append((a, op, b, out))
    return wires, gates


class Graph:
    def __init__(self):
        self.wires = {}
        self.inputs = set()
        self.outputs = {}
        self.size = None

    def add_wires(self, wires):
        for name, value in wires:
            self.wires[name] = value
            self.inputs.add(name)
        self.size = len(self.wires) // 2

    def add_gates(self, gates):
        for a, op, b, out in gates:
            match op:
                case 'AND':
                    fn = and_
                case 'OR':
                    fn = or_
                case 'XOR':
                    fn = xor

            self.outputs[out] = (fn, a, b)
            if out not in self.wires:
                self.wires[out] = None

    def resolve_wire(self, wire):
        value = self.wires.get(wire)
        if value is not None:
            return value

        assert wire in self.outputs
        fn, a, b = self.outputs[wire]
        value = fn(self.resolve_wire(a), self.resolve_wire(b))
        return value

    def describe_wire(self, wire):
        if self.wires.get(wire) is not None:
            return wire

        fn, a, b = self.outputs[wire]
        op = '&' if fn is and_ else '^' if fn is xor else '|'

        a, b = sorted((a, b))
        left = self.describe_wire(a)
        right = self.describe_wire(b)
        return f'({left} {op} {right})'

    def get_result(self):
        wires = [x for x in self.wires.keys() if x.startswith('z')]
        wires.sort()
        result = 0
        for n in range(len(wires)):
            wire = wires[n]
            try:
                value = self.resolve_wire(wire)
            except RecursionError:
                return None
            result += value << n
        return result

    def get_input_value(self, prefix: str):
        wires = [x for x in self.wires.keys() if x.startswith(prefix)]
        wires.sort()
        result = 0
        for n in range(len(wires)):
            wire = wires[n]
            result += self.wires[wire] * (2 ** n)
        return result

    def find_connected_inputs(self, wire):
        q = deque()
        q.append(wire)
        result = set()
        visited = set()
        while q:
            wire = q.popleft()
            if wire in self.inputs:
                result.add(wire)
                continue

            _, a, b = self.outputs[wire]
            for n in (a, b):
                if n not in visited:
                    q.append(n)
                    visited.add(n)
        return result

    def swap_outputs(self, a, b):
        a_gate = self.outputs[a]
        self.outputs[a] = self.outputs[b]
        self.outputs[b] = a_gate


def run(stream, test: bool = False):
    with timing("Part 1"):
        wires, gates = parse(stream)
        graph = Graph()
        graph.add_wires(wires)
        graph.add_gates(gates)
        result1 = graph.get_result()

    with timing("Part 2"):
        # I did not come up with a sensible general programmatic solution to
        # this Part 2, I just inspected the input and traced out the broken
        # paths with pen & paper.
        result2 = 0

    return (result1, result2)
