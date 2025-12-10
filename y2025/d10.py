"""Advent of Code 2025

Day 10: Factory

https://adventofcode.com/2025/day/10
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing, INF, PriorityQueue


def toggle(lights, button):
    return tuple(
        not x if i in button else x
        for i, x in enumerate(lights))


def jolt(counters, button):
    return tuple(
            x + 1 if i in button else x
            for i, x in enumerate(counters))


def get_distance(counters, goal):
    return sum(goal[i] - x for i, x in enumerate(counters))


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

    def find_joltage_path(self):
        # Use an AStar to find the shortest path from the starting state to the
        # goal
        start = tuple(0 for _ in self.joltages)
        goal = self.joltages

        q = PriorityQueue()
        q.push(start, get_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        explored = set()

        while q:
            est, node = q.pop()

            if node == goal:
                return est

            score = dist[node] + 1
            for b in self.buttons:
                n = jolt(node, b)
                if n in explored:
                    continue
                # Prune any branches where one of the counters has gone over
                # the target joltage. Since there's no way to *reduce* a
                # joltage, these branches cannot ever find a solution.
                if any(x > goal[i] for i, x in enumerate(n)):
                    continue
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_distance(n, goal)
                    q.set_priority(n, f)
            explored.add(node)
        raise Exception(f"No solution found for {goal}")


def parse(stream) -> str:
    machines = []
    for line in stream:
        words = line.strip().split()
        lights = words[0][1:-1]  # Strip off square brackets
        targets = {i for i, x in enumerate(lights) if x == '#'}
        buttons = [set(map(int, x[1:-1].split(','))) for x in words[1:-1]]
        joltages = tuple(map(int, words[-1][1:-1].split(',')))
        machine = Machine(len(lights), targets, buttons, joltages)
        machines.append(machine)
    return machines


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(x.find_light_path() for x in parsed)

    with timing("Part 2"):
        result2 = sum(x.find_joltage_path() for x in parsed)

    return (result1, result2)
