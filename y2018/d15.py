"""Advent of Code 2018

Day 15: Beverage Bandits

https://adventofcode.com/2018/day/15
"""
import logging  # noqa: F401
from collections import defaultdict

from util import get_manhattan_distance, timing, INF, PriorityQueue


def get_adjacent(position: tuple) -> set[tuple]:
    y, x = position
    return {(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)}


class Unit:
    def __init__(
            self, key: int, side: bool, position: tuple,
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
        self.distance = defaultdict(lambda: defaultdict(lambda: INF))

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
            y += 1

    @property
    def elves(self):
        return self.units[True].values()

    @property
    def goblins(self):
        return self.units[False].values()

    def find_targets(self, unit: Unit) -> list:
        targets = self.units[not unit.side].values()
        return list(targets)

    def get_neighbours(self, position: tuple) -> set:
        return get_adjacent(position) - (self.walls | self.occupied)

    def find_path(
            self, start: tuple, goal: tuple,
            limit: int | float = INF,
            ) -> int | None:
        """Find the shortest path from `start` to `goal`.

        Return the number of steps in the shortest path, or None if the goal is
        not reachable.

        Retain the shortest distance to each point we explore in an instance
        attribute of the Game, so we can avoid re-calculating them later.

        If the path cost exceeds `limit`, give up and return None.
        """
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        dist = self.distance[start]
        dist[start] = 0
        explored = set()

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            for n in self.get_neighbours(node):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
            explored.add(node)
        return None

    def select_move(self, start: tuple, goals: set) -> tuple | None:
        """Select a target square for unit movement.

        If the unit is currently at `start`, and its possible destinations are
        listed in `goals`, select the best goal to move towards, or None if
        none of those goals can be reached.
        """
        if len(goals) == 0:
            return None
        if len(goals) == 1:
            dest = tuple(goals)[0]
            cost = self.find_path(start, dest)
            return dest if cost is not None else None

        best = INF
        result = None
        # Sort the goals by manhattan distance and reading order first, then
        # use A Star to determine the shortest path to each one. To save on
        # cycles, once we have found a shortest path, abandon any goals that
        # can't be resolved in fewer steps. In the worst case, the goal with
        # the shortest manhattan will be unreachable, then we will end up
        # exploring the entire space. But at least we will have cached those
        # results for the next attempt.
        goals = list(goals)
        goals.sort(key=lambda x: (get_manhattan_distance(start, x), x))
        for goal in goals:
            cost = self.find_path(start, goal, best)
            if cost is not None and cost < best:
                result = goal
                best = cost
        return result

    def select_step(self, start: tuple, goal: tuple) -> tuple:
        """Select the next step towards the selected goal.

        Considering all of the open squares adjacent to `start`, choose the one
        that has the shortest distance to the goal, breaking ties in favour of
        the earliest reading order.
        """
        best = INF
        choices = []
        for n in self.get_neighbours(start):
            cost = self.find_path(n, goal, best)
            if cost is not None and cost < best:
                best = cost
                choices.append((cost, n))
        choices.sort()
        return choices[0][1]

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
            logging.debug(f"Not moving {unit.key}, already in range")
            return False

        target_adjacencies = set()
        for pos in target_positions:
            target_adjacencies |= get_adjacent(pos)
        target_adjacencies -= (self.walls | self.occupied)
        if not target_adjacencies:
            logging.debug(f"Not moving {unit.key}, nowhere to go")
            return False

        goal = self.select_move(unit.position, target_adjacencies)
        if goal is None:
            logging.debug(f"Not moving {unit.key}, cannot reach")
            return False

        pos = self.select_step(unit.position, goal)
        logging.debug(f"Moving {unit.key} {unit.position} -> {pos}")
        self.occupied.discard(unit.position)
        self.occupied.add(pos)
        unit.position = pos
        return True

    def do_round(self) -> bool:
        """Do a round of combat.

        Return whether the game has ended during this round.
        """
        units = list(self.elves) + list(self.goblins)
        units.sort(key=lambda x: x.position)
        for unit in units:
            targets = self.find_targets(unit)
            if not targets:
                return False
            self.do_move(unit, targets)


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = Game()
        game.parse(stream)
        game.do_round()
        result1 = 0

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
