"""Advent of Code 2018

Day 23: Experimental Emergency Teleportation

https://adventofcode.com/2018/day/23
"""
import logging  # noqa: F401
from collections import namedtuple
from itertools import combinations

from util import get_manhattan_distance, timing


P = namedtuple('P', ('x', 'y', 'z'))
Bot = namedtuple('Bot', ('p', 'r'))


def has_intersection(a: Bot, b: Bot) -> bool:
    """Return whether any points are in range of both bots."""
    totalr = a.r + b.r
    return get_manhattan_distance(a.p, b.p) <= totalr


def all_intersects(bots: tuple[Bot]) -> bool:
    """Return whether any points are in range of all bots.

    Return False if any of the bots is fully disjoint with any of the other
    bots.
    """
    for a, b in combinations(bots, 2):
        if not has_intersection(a, b):
            return False
    return True


class Swarm:
    def __init__(self):
        self.bots = {}

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        for line in stream:
            line = line.strip()
            if line == '':
                continue

            parts = line.strip().split(', ')
            coords = parts[0][5:-1].split(',')
            pos = tuple(int(x) for x in coords)
            radius = int(parts[1].split('=')[1])
            self.bots[pos] = Bot(pos, radius)

    def get_strongest(self) -> Bot:
        bots = [(b.r, b) for b in self.bots.values()]
        bots.sort(reverse=True)
        return bots[0][1]

    def count_in_range(self, bot: Bot) -> int:
        return sum(
                int(get_manhattan_distance(bot.p, k) <= bot.r)
                for k in self.bots)

    def count_in_range_of(self, position: tuple) -> int:
        return sum(
                int(get_manhattan_distance(position, b.p) <= b.r)
                for b in self.bots.values())


def parse(stream) -> Swarm:
    swarm = Swarm()
    swarm.parse(stream)
    return swarm


def run(stream, test: bool = False):
    with timing("Part 1"):
        swarm = parse(stream)
        bot = swarm.get_strongest()
        result1 = swarm.count_in_range(bot)

    with timing("Part 2"):
        if test:
            swarm = parse(
                    """
                    pos=<10,12,12>, r=2
                    pos=<12,14,12>, r=2
                    pos=<16,12,12>, r=4
                    pos=<14,14,14>, r=6
                    pos=<50,50,50>, r=200
                    pos=<10,10,10>, r=5
                    """)
        result2 = 0

    return (result1, result2)
