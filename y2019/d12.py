"""Advent of Code 2019

Day 12: The N-Body Problem

https://adventofcode.com/2019/day/12
"""
import logging  # noqa: F401
from itertools import combinations

from util import timing


class Body:
    def __init__(self, position: tuple):
        self.position = list(position)
        self.velocity = [0, 0, 0]

    def apply_gravity(self, other):
        for i, p in enumerate(self.position):
            q = other.position[i]
            if p != q:
                self.velocity[i] += 1 if p < q else -1

    def apply_velocity(self):
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i]

    @property
    def potential_energy(self):
        return sum(abs(p) for p in self.position)

    @property
    def kinetic_energy(self):
        return sum(abs(v) for v in self.velocity)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


class System:
    def __init__(self):
        self.bodies = []

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            # remove the angle brackets
            line = line[1:-1]
            axes = line.split(', ')
            pos = (int(x.split('=')[1]) for x in axes)
            self.bodies.append(Body(pos))

    def update(self):
        """Update the system by one time tick."""
        for a, b in combinations(self.bodies, 2):
            a.apply_gravity(b)
            b.apply_gravity(a)
        for body in self.bodies:
            body.apply_velocity()

    def run(self, steps: int):
        for i in range(steps):
            self.update()

    def get_total_energy(self) -> int:
        return sum(x.total_energy for x in self.bodies)


def parse(stream) -> System:
    result = System()
    result.parse(stream)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        system = parse(stream)
        steps = 10 if test else 1000
        system.run(steps)
        result1 = system.get_total_energy()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
