"""Advent of Code 2019

Day 12: The N-Body Problem

https://adventofcode.com/2019/day/12
"""
import logging  # noqa: F401
from copy import deepcopy
from itertools import combinations
from math import lcm

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

    def to_tuple(self) -> tuple:
        return (*self.position, *self.velocity)


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

    def find_cycles(self) -> dict:
        """Run the system looking for cycles in each body's movement.

        Continue updating until we have identified a cycle for every body, and
        return the lengths of those cycles as a dict, mapping each body's index
        to its cycle length.
        """
        cycles = {}
        history = {}
        for i in range(3):
            state = tuple((x.position[i], x.velocity[i]) for x in self.bodies)
            history[i] = {state: 0}
        t = 0
        while len(cycles) < 3:
            self.update()
            t += 1

            for i in range(3):
                state = tuple(
                        (x.position[i], x.velocity[i]) for x in self.bodies)
                # Is this axis in a state it has previously occupied?
                if state in history[i]:
                    if i not in cycles:
                        cycles[i] = t - history[i][state]
                        logging.debug(
                                f"Found cycle for {'XYZ'[i]} at t {t}, "
                                f"length {cycles[i]}")
                history[i][state] = t
        return cycles

    def get_total_energy(self) -> int:
        return sum(x.total_energy for x in self.bodies)


def parse(stream) -> System:
    result = System()
    result.parse(stream)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        system = parse(stream)
        orig = deepcopy(system)
        steps = 10 if test else 1000
        system.run(steps)
        result1 = system.get_total_energy()

    with timing("Part 2"):
        system = orig
        cycles = system.find_cycles()
        result2 = lcm(*cycles.values())

    return (result1, result2)
