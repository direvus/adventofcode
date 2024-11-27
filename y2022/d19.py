"""Advent of Code 2022

Day 19: Not Enough Minerals

https://adventofcode.com/2022/day/19
"""
import logging  # noqa: F401
from collections import deque
from math import ceil, prod
from operator import sub

from util import timing


MATERIALS = (
        'geode',
        'obsidian',
        'clay',
        'ore',
        )
SIZE = len(MATERIALS)


class Blueprint:
    def __init__(self, bpid):
        self.id = bpid
        self.recipes = {}
        self.maxcosts = []

    def add_recipe(self, output, inputs):
        index = MATERIALS.index(output)
        materials = []
        for name in MATERIALS:
            materials.append(inputs.get(name, 0))
        self.recipes[index] = tuple(materials)

    def get_time_to_build(self, target, robots, materials) -> int:
        """Return the amount of time until we can build `target`.

        If we can already build it, return zero. Otherwise, return the number
        of time units we need to wait at the current rate of production before
        we can build one target robot.

        If the current production will never yield the materials needed to
        produce a target robot, return None.
        """
        recipe = self.recipes[target]
        if all(materials[i] >= recipe[i] for i in range(SIZE)):
            return 0
        if any(recipe[i] > 0 and robots[i] == 0 for i in range(SIZE)):
            return None

        result = 0
        for i in range(SIZE):
            if recipe[i] == 0:
                continue
            required = recipe[i] - materials[i]
            time = ceil(required / robots[i])
            if time > result:
                result = time
        return result

    def get_max_cost(self, material: int) -> int:
        """Return the maximum cost for a particular material."""
        return max(x[material] for x in self.recipes.values())

    def find_maximum_geodes(self, limit: int = 24) -> int:
        """Find the maximum number of geodes this blueprint could open.

        Given a time limit of `limit` units, determine and return the maximum
        number of geodes that could be opened using the recipes in this
        blueprint.
        """
        maxcosts = tuple(self.get_max_cost(i) for i in range(SIZE))
        start = (0, (0, 0, 0, 1), (0, 0, 0, 0))
        best = 0
        q = deque()
        q.append(start)
        while q:
            node = q.popleft()
            time, robots, materials = node

            remain = limit - time
            if robots[0] > 0:
                geodes = materials[0] + remain * robots[0]
                if geodes > best:
                    best = geodes

            # Get an upper limit on how many geodes we could possibly produce
            # from here -- if we did nothing but build geode-cracking robots
            # every minute until the time limit. If that number doesn't beat
            # the best solution found so far, we can abandon this branch.
            if remain == 1:
                maxgeodes = materials[0] + robots[0]
                if maxgeodes <= best:
                    continue
            elif remain > 0:
                maxgeodes = materials[0]
                bots = robots[0]
                for _ in range(remain):
                    maxgeodes += bots
                    bots += 1
                if maxgeodes <= best:
                    continue

            for i in range(SIZE):
                wait = self.get_time_to_build(i, robots, materials)
                if wait is None or wait + 1 >= remain:
                    continue

                # For resources other than geode, do a quick heuristic to see
                # if there is any point building more robots.
                if i != 0:
                    # Figure out the amount of this material we'd need, if we
                    # did nothing but build the most expensive recipe for this
                    # material every turn until the time limit.
                    cost = maxcosts[i]
                    maxreq = cost * remain
                    # Figure out the amount of the material we will have by the
                    # time limit, if we don't build any extra robots to produce
                    # it.
                    final = remain * robots[i] + materials[i]
                    if final >= maxreq:
                        # Building extra robots of this type cannot possibly
                        # provide any benefit.
                        continue

                gain = map(lambda x, y: x + y * (wait + 1), materials, robots)
                mats = map(sub, gain, self.recipes[i])
                prod = tuple(
                        r + 1 if i == j else r
                        for j, r in enumerate(robots))
                q.append((time + wait + 1, tuple(prod), tuple(mats)))
        return best

    def find_quality(self, limit: int = 24):
        geodes = self.find_maximum_geodes(limit)
        return geodes * self.id


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip().strip('.')
        title, content = line.split(': ')
        bpid = int(title.split()[1])
        bp = Blueprint(bpid)
        for recipe in content.split('. '):
            intro, costs = recipe.split(' costs ')
            output = intro.split()[1]
            inputs = {}
            for cost in costs.split(' and '):
                quantity, material = cost.split()
                inputs[material] = int(quantity)
            bp.add_recipe(output, inputs)
        result.append(bp)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        blueprints = parse(stream)
        levels = [x.find_quality() for x in blueprints]
        result1 = sum(levels)

    with timing("Part 2"):
        if not test:
            # Part 2 is too slow for automated test runs, and besides, it
            # doesn't touch any code paths that aren't already tested by Part
            # 1.
            geodes = [x.find_maximum_geodes(32) for x in blueprints[:3]]
            result2 = prod(geodes)
        else:
            result2 = 0

    return (result1, result2)
