#!/usr/bin/env python
import heapq
import sys
from collections import defaultdict, namedtuple

from util import timing


Pulse = namedtuple('pulse', ['depth', 'high', 'source', 'dest'])


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def __bool__(self):
        return bool(self.queue)

    def push(self, task):
        heapq.heappush(self.queue, task)

    def has_task(self, task):
        return task in self.queue

    def pop(self):
        return heapq.heappop(self.queue)


class Module:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    def handle_pulse(self, pulse: Pulse) -> list[Pulse]:
        return []


class Broadcast(Module):
    def handle_pulse(self, pulse: Pulse):
        return [Pulse(pulse.depth + 1, pulse.high, self.name, dest)
                for dest in self.targets]


class FlipFlop(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = False

    def handle_pulse(self, pulse: Pulse) -> list[Pulse]:
        if pulse.high:
            return []
        self.state = not self.state
        return [Pulse(pulse.depth + 1, self.state, self.name, dest)
                for dest in self.targets]


class Conjunction(Module):
    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.inputs = defaultdict(lambda: False)

    def add_input(self, name: str) -> None:
        self.inputs[name] = False

    def handle_pulse(self, pulse: Pulse) -> list[Pulse]:
        self.inputs[pulse.source] = pulse.high
        high = False in self.inputs.values()
        return [Pulse(pulse.depth + 1, high, self.name, dest)
                for dest in self.targets]


def parse_modules(stream) -> dict:
    modules = {}
    watchers = set()
    for line in stream:
        line = line.strip()
        name, targets = line.split(' -> ')
        targets = targets.split(', ')

        cls = Module
        if name[0] == '%':
            cls = FlipFlop
            name = name[1:]
        elif name[0] == '&':
            cls = Conjunction
            name = name[1:]
            watchers.add(name)
        elif name == 'broadcaster':
            cls = Broadcast

        module = cls(name, targets)
        modules[name] = module

    for name, module in modules.items():
        for target in module.targets:
            if target in watchers:
                modules[target].add_input(name)
    return modules


def push_button(modules: dict) -> tuple[int, int]:
    pq = PriorityQueue()
    pulse = Pulse(0, False, 'button', 'broadcaster')
    pq.push(pulse)
    totals = defaultdict(lambda: 0)
    while pq:
        pulse = pq.pop()
        totals[pulse.high] += 1
        if pulse.dest not in modules:
            continue
        module = modules[pulse.dest]
        outputs = module.handle_pulse(pulse)
        for output in outputs:
            pq.push(output)
    return (totals[False], totals[True])


if __name__ == '__main__':
    modules = parse_modules(sys.stdin)

    # Part 1
    with timing("Part 1"):
        low, high = (0, 0)
        for _ in range(1000):
            result = push_button(modules)
            low += result[0]
            high += result[1]
        result = low * high
    print(f"Result for Part 1 = {result} \n")

    # Part 2
    with timing("Part 2"):
        result = 0
    print(f"Result for Part 2 = {result} \n")
