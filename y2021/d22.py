"""Advent of Code 2021

Day 22: Reactor Reboot

https://adventofcode.com/2021/day/22
"""
import logging  # noqa: F401

from util import timing


def disjoint(a: tuple, b: tuple) -> bool:
    return (
            a[1] < b[0] or b[1] < a[0] or
            a[3] < b[2] or b[3] < a[2] or
            a[5] < b[4] or b[5] < a[4])


def contains(a: tuple, b: tuple) -> bool:
    return (
            a[0] <= b[0] and a[1] >= b[1] and
            a[2] <= b[2] and a[3] >= b[3] and
            a[4] <= b[4] and a[5] >= b[5])


def get_volume(box: tuple) -> int:
    return (
            (box[1] - box[0] + 1) *
            (box[3] - box[2] + 1) *
            (box[5] - box[4] + 1))


def get_total_volume(boxes: tuple) -> int:
    return sum(get_volume(box) for box in boxes)


def divide_axis(box: tuple, axis: int, low: int, high: int) -> tuple:
    i = axis * 2
    a, b = box[i: i + 2]
    if high < a or low > b:
        return box, set()

    outers = set()
    if low > a:
        new = list(box)
        new[i + 1] = low - 1
        outers.add(tuple(new))

        box = list(box)
        box[i] = low

    if high < b:
        new = list(box)
        new[i] = high + 1
        outers.add(tuple(new))

        box = list(box)
        box[i + 1] = high

    return tuple(box), outers


def divide(a: tuple, b: tuple) -> set[tuple]:
    result = set()
    for axis in range(3):
        i = axis * 2
        low, high = b[i: i + 2]
        inner, outers = divide_axis(a, axis, low, high)
        result |= outers
        a = inner
    result.add(a)
    return result


class Grid:
    def __init__(self):
        self.active = set()

    @property
    def total_active(self) -> int:
        return sum(get_volume(x) for x in self.active)

    def divide(self, box: tuple):
        """Split up the active regions in this grid.

        Without changing the set of individual active cubes, break up the
        active region cuboids as needed to ensure that all of them are either
        fully disjoint from, or fully contained by, the given `box`.
        """
        new = set()
        for x in self.active:
            if disjoint(x, box):
                new.add(x)
                continue
            new |= divide(x, box)
        self.active = new

    def activate(self, box: tuple):
        if all(disjoint(x, box) for x in self.active):
            # Simple, it is a standalone new cuboid.
            self.active.add(box)
            return

        self.divide(box)
        remove = set()
        for contact in self.active:
            if disjoint(contact, box):
                continue
            if contains(contact, box):
                # Wholly contained by an existing cuboid, no action required.
                return
            elif contains(box, contact):
                # Wholly contains an existing cuboid, delete the existing one.
                remove.add(contact)
        self.active -= remove
        self.active.add(box)

    def deactivate(self, box: tuple):
        if all(disjoint(x, box) for x in self.active):
            # No overlaps, all these cubes are already off, do nothing.
            return

        self.divide(box)
        remove = set()
        for contact in self.active:
            if disjoint(contact, box):
                continue
            if contains(box, contact):
                # Wholly contains an existing cuboid, remove it.
                remove.add(contact)
        self.active -= remove

    def do_updates(self, updates: list):
        for state, box in updates:
            if state:
                self.activate(box)
            else:
                self.deactivate(box)


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        state, box = line.split()
        axes = box.split(',')
        coords = []
        for axis in axes:
            _, r = axis.split('=')
            coords.extend(sorted(int(x) for x in r.split('..')))
        result.append((state == 'on', tuple(coords)))
    return result

    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        bounds = (-50, 50, -50, 50, -50, 50)
        part1 = filter(lambda x: not disjoint(x[1], bounds), parsed)
        grid = Grid()
        grid.do_updates(part1)

        result1 = grid.total_active

    with timing("Part 2"):
        grid = Grid()
        grid.do_updates(parsed)
        result2 = grid.total_active

    return (result1, result2)
