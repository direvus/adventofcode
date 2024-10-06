"""Advent of Code 2018

Day 23: Experimental Emergency Teleportation

https://adventofcode.com/2018/day/23
"""
import logging  # noqa: F401

from util import get_manhattan_distance, timing


class Swarm:
    def __init__(self):
        self.bots = {}

    def parse(self, stream):
        for line in stream:
            parts = line.strip().split(', ')
            coords = parts[0][5:-1].split(',')
            pos = tuple(int(x) for x in coords)
            radius = int(parts[1].split('=')[1])
            self.bots[pos] = radius

    def get_strongest(self) -> tuple:
        bots = [(v, k) for k, v in self.bots.items()]
        bots.sort()
        return bots[-1][1]

    def count_in_range(self, position: tuple, radius: int) -> int:
        return sum(
                int(get_manhattan_distance(position, k) <= radius)
                for k in self.bots)


def parse(stream) -> Swarm:
    swarm = Swarm()
    swarm.parse(stream)
    return swarm


def run(stream, test: bool = False):
    with timing("Part 1"):
        swarm = parse(stream)
        pos = swarm.get_strongest()
        radius = swarm.bots[pos]
        result1 = swarm.count_in_range(pos, radius)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
