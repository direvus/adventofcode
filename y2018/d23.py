"""Advent of Code 2018

Day 23: Experimental Emergency Teleportation

https://adventofcode.com/2018/day/23
"""
import logging  # noqa: F401
from collections import namedtuple
from itertools import combinations
from math import prod

from util import NINF, PriorityQueue, get_manhattan_distance, timing


P = namedtuple('P', ('x', 'y', 'z'))
Bot = namedtuple('Bot', ('p', 'r'))
Box = namedtuple('Box', ('a', 'b'))


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


class Box:
    def __init__(self, a: P, b: P):
        # If necessary, swap the points so that `a` is always the corner
        # closest to negative infinity.
        if sum(a) > sum(b):
            b, a = a, b
        self.a = a
        self.b = b
        self.axes = []

        for i in range(3):
            m, n = self.a[i], self.b[i]
            if m > n:
                m, n = n, m
            self.axes.append((m, n))

    def __str__(self):
        return f"{tuple(self.a)} - {tuple(self.b)}"

    @property
    def volume(self) -> int:
        return prod(abs(self.b[i] - self.a[i]) + 1 for i in range(3))

    @property
    def major_axis(self) -> int:
        """Return the largest axis of this box as an integer.

        The result is the axis in which this box has the longest edges, with
        0 = x, 1 = y and 2 = z.
        """
        longest = NINF
        result = None
        for i in range(3):
            length = abs(self.b[i] - self.a[i]) + 1
            if length > longest:
                longest = length
                result = i
        return result

    def contains(self, point: P) -> bool:
        for i, (m, n) in enumerate(self.axes):
            if m > point[i] or n < point[i]:
                return False
        return True

    def distance(self, point: P) -> int:
        """Return the distance between this box and a point.

        Return the distance between the target point and the nearest point to
        it that lies within the box. This is zero for any target points
        that are themselves contained in the box.
        """
        result = 0
        for i, (m, n) in enumerate(self.axes):
            if m > point[i]:
                result += m - point[i]
            elif n < point[i]:
                result += point[i] - n
            # Otherwise, it is within the bounds of this axis, so add nothing.
        return result

    def split(self) -> tuple[Box, Box]:
        """Split this box into two roughly equally-sized boxes.

        Find the largest axis of the box, and cut it roughly in half
        across that axis.

        Should not be called on a box that only contains a single point, i.e.,
        check the volume is greater than one before cutting.
        """
        i = self.major_axis
        length = abs(self.b[i] - self.a[i]) + 1
        half = self.a[i] + length // 2
        a2 = list(self.a)
        b1 = list(self.b)
        a2[i] = half
        b1[i] = half - 1
        r1 = Box(self.a, P(*b1))
        r2 = Box(P(*a2), self.b)
        return (r1, r2)


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

    def count_in_range_of(self, point: P) -> int:
        return sum(
                int(get_manhattan_distance(point, b.p) <= b.r)
                for b in self.bots.values())

    def get_bounding_box(self) -> Box:
        """Return a Box that includes all of the bots."""
        locs = list(self.bots.keys())
        locs.sort(key=lambda x: sum(x))
        return Box(locs[0], locs[-1])

    def count_overlaps(self, box: Box) -> int:
        """Return the number of bots that overlap a Box.

        This includes all bots that are located within the Box, and also all
        bots that are in range of some point within the Box.
        """
        result = 0
        for bot in self.bots.values():
            if box.distance(bot.p) <= bot.r:
                result += 1
        return result

    def find_optimal_points(self) -> set[P]:
        """Return the set of points that are in range of the most bots."""
        # Start with a Box that includes all of the bots, and progressively
        # slice it into smaller boxes, until we have boxes that only contain
        # single points, and rejecting branch paths along the way that can't
        # improve upon the best score found so far for a single point.
        result = set()
        box = self.get_bounding_box()
        q = PriorityQueue()
        best = NINF
        result = set()
        boxes = {0: box}
        q.push(0, (-self.count_overlaps(box), box.volume))
        i = 1
        while q:
            (bots, vol), k = q.pop()
            bots = -bots
            box = boxes.pop(k)
            if bots < best:
                # This box can't possibly contain any winning points, discard
                # it.
                continue

            if vol == 1:
                # the box contains a single point.
                pos = box.a
                if bots > best:
                    # Best score so far, replace the winning list with this
                    # point.
                    result = {pos}
                    best = bots
                elif bots == best:
                    # Tied for best score, add it to the winning list.
                    result.add(pos)
                continue

            # Break the box into smaller boxes and put them into the queue.
            # Prioritise boxes based on the number of bots overlapping the box
            # (more bots first), followed by their volume (smaller boxes
            # first).
            for subbox in box.split():
                boxes[i] = subbox
                vol = subbox.volume
                count = self.count_overlaps(subbox)
                q.set_priority(i, (-count, vol))
                i += 1
        return result


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
        points = list(swarm.find_optimal_points())
        distances = map(lambda x: sum(abs(c) for c in x), points)
        result2 = min(distances)

    return (result1, result2)
