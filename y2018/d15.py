"""Advent of Code 2018

Day 15: Beverage Bandits

https://adventofcode.com/2018/day/15
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing


def get_adjacent(position: tuple) -> set[tuple]:
    y, x = position
    return {(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)}


class Unit:
    def __init__(
            self, key: int, position: tuple, side: bool,
            power: int = 3, health: int = 200):
        self.key = key
        self.position = position
        self.side = side
        self.power = power
        self.health = health


class Game:
    def __init__(self):
        self.walls = set()
        self.occupied = set()
        self.units = defaultdict(dict)

    def parse(self, stream):
        y = 0
        unitkey = 0
        for line in stream:
            line = line.strip()
            for x, ch in enumerate(line):
                pos = (y, x)
                match ch:
                    case '#':
                        self.walls.add(pos)
                    case 'E' | 'G':
                        side = ch == 'E'
                        unit = Unit(unitkey, side, pos)
                        unitkey += 1
                        self.units[side][unitkey] = unit
                        self.occupied.add(pos)

    @property
    def elves(self):
        return self.units[True].values()

    @property
    def goblins(self):
        return self.units[False].values()

    def find_targets(self, unit: Unit) -> list:
        targets = self.units[not unit.side].values()
        return list(targets)

    def do_move(self, unit: Unit, targets: list[Unit]) -> bool:
        """Perform this unit's movement.

        If one of the targets is already adjacent to the unit, then no movement
        is needed, return without moving.

        Otherwise, consider all of the open squares that are adjacent to each
        target. If there are none available, return without moving.

        Eliminate destination squares that are not reachable. If no valid
        destinations remain, return without moving.

        Finally, select the destination square that can be reached in the
        fewest steps, breaking ties in reading order. Move one step towards
        that square along the shortest path, again breaking ties by
        preferencing squares with a lower reading order.

        Return whether the unit moved.
        """
        adjacent = get_adjacent(unit.position)
        target_positions = {x.position for x in targets}
        if target_positions & adjacent:
            return False

        target_adjacencies = set()
        for pos in target_positions:
            target_adjacencies |= get_adjacent(pos)
        target_adjacencies -= (self.walls | self.occupied)
        if not target_adjacencies:
            return False

        # Now it's time for some pathfinding.

    def do_round(self) -> bool:
        """Do a round of combat.

        Return whether the game has ended during this round.
        """
        units = list(self.elves) + list(self.goblins)
        units.sort(lambda x: x.position)
        for unit in units:
            targets = self.find_targets(unit)
            if not targets:
                return False
            self.do_move(unit, targets)


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = Game()
        game.parse(stream)
        result1 = 0

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
