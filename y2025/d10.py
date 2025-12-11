"""Advent of Code 2025

Day 10: Factory

https://adventofcode.com/2025/day/10
"""
import logging  # noqa: F401
from collections import defaultdict

from scipy.optimize import linprog

from util import timing, INF, PriorityQueue


def toggle(lights, button):
    return tuple(
        not x if i in button else x
        for i, x in enumerate(lights))


class Machine:
    def __init__(self, lights: int, targets: set, buttons: tuple, joltages: tuple):
        self.lights = lights
        self.targets = targets
        self.buttons = buttons
        self.joltages = joltages

    def find_light_path(self):
        # Use a Dijkstra to find the shortest path from the starting state to
        # the goal
        start = tuple(False for _ in range(self.lights))
        goal = tuple(i in self.targets for i in range(self.lights))

        q = PriorityQueue()
        q.push(start, 0)
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        explored = set()

        while q:
            cost, node = q.pop()

            if node == goal:
                return cost

            score = cost + 1
            for b in self.buttons:
                n = toggle(node, b)
                if n in explored:
                    continue
                if score < dist[n]:
                    dist[n] = score
                    q.set_priority(n, score)
            explored.add(node)
        raise Exception(f"No solution found for {goal}")

    def get_button_span(self):
        n = len(self.joltages)
        for i in range(len(self.joltages)):
            count = sum(int(i in b) for b in self.buttons)
            if count < n:
                n = count
        return n

    def find_joltage_presses(self):
        width = len(self.buttons)
        c = [1] * width
        a = [
                [int(i in b) for b in self.buttons]
                for i in range(len(self.joltages))]

        res = linprog(
                c=c, A_eq=a, b_eq=self.joltages,
                method='highs', integrality=1)
        if not res.success:
            raise Exception("Failed to find a solution!")

        return round(res.fun)


def parse(stream) -> str:
    machines = []
    for line in stream:
        words = line.strip().split()
        lights = words[0][1:-1]  # Strip off square brackets
        targets = {i for i, x in enumerate(lights) if x == '#'}
        buttons = [frozenset(map(int, x[1:-1].split(','))) for x in words[1:-1]]
        joltages = tuple(map(int, words[-1][1:-1].split(',')))
        machine = Machine(len(lights), targets, buttons, joltages)
        machines.append(machine)
    return machines


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(x.find_light_path() for x in parsed)

    with timing("Part 2"):
        counts = defaultdict(lambda: 0)
        for x in parsed:
            diff = len(x.joltages) - len(x.buttons)
            counts[diff] += 1

        result2 = sum(x.find_joltage_presses() for x in parsed)

    return (result1, result2)
