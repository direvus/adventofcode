"""Advent of Code 2022

Day 15: Beacon Exclusion Zone

https://adventofcode.com/2022/day/15
"""
import logging  # noqa: F401
import re

from spans import SpanSet
from util import get_manhattan_distance, timing


def disjoint(a: tuple, b: tuple):
    return (a[1] < b[0] or b[1] < a[0] or
            a[3] < b[2] or b[3] < a[2])


def contains(a: tuple, b: tuple):
    return (a[0] <= b[0] and a[1] >= b[1] and
            a[2] <= b[2] and a[3] >= b[3])


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
    for axis in range(2):
        i = axis * 2
        low, high = b[i: i + 2]
        inner, outers = divide_axis(a, axis, low, high)
        result |= outers
        a = inner
    result.add(a)
    return result


def get_rect(center: tuple, r: int) -> tuple:
    """Get a rectangular representation of a sensor region.

    The return is a 4-tuple of the boundaries of the sensor region, in
    (SW, NE, NW, SE) order.

    These diagonal boundaries are each expressed as a single integer.  For SW
    and NE boundaries it is the difference between the X and Y values at every
    point along those lines, and for NW and SE, it is the sum of the X and Y
    values.
    """
    left = center[0] - r
    top = center[1] - r
    bottom = center[1] + r
    return (
            left - center[1],
            center[0] - top,
            left + center[1],
            center[0] + bottom,
            )


def subtract_rect(regions: set, rect: tuple) -> set:
    """Remove a rectangular region from a set of rectangular regions.

    Return a new set of regions that excludes all of the space contained by
    `rect`.
    """
    result = set()
    for region in regions:
        if disjoint(region, rect):
            result.add(region)
            continue
        # Split the region up into subregions so that each subregion is either
        # fully disjoint from, or fully contained by, `rect`. Then, add only
        # those regions that are disjoint to the final result.
        subs = divide(region, rect)
        result |= {x for x in subs if disjoint(x, rect)}
    return result


class Grid:
    def __init__(self):
        self.sensors = set()
        self.beacons = set()
        self.detections = {}
        self.ranges = {}
        self.maxrange = 0
        self.minx = 0
        self.maxx = 0

    def load_coords(self, coords):
        for sensor, beacon in coords:
            self.sensors.add(sensor)
            self.beacons.add(beacon)
            self.detections[sensor] = beacon
            dist = get_manhattan_distance(sensor, beacon)
            if dist > self.maxrange:
                self.maxrange = dist
            self.ranges[sensor] = dist

        allpoints = self.sensors | self.beacons
        self.minx = min(p[0] for p in allpoints)
        self.maxx = max(p[0] for p in allpoints)

    def is_beacon_possible(self, position: tuple) -> bool:
        if position in self.beacons:
            return True
        if position in self.sensors:
            return False
        for sensor in self.sensors:
            r = self.ranges[sensor]
            d = get_manhattan_distance(sensor, position)
            if d <= r:
                return False
        return True

    def get_sensor_slice(self, sensor: tuple, y: int) -> tuple | None:
        r = self.ranges[sensor]
        ydiff = abs(y - sensor[1])
        if ydiff > r:
            return None
        low = sensor[0] - r + ydiff
        high = sensor[0] + r - ydiff
        return (low, high)

    def count_possible(self, y: int) -> int:
        spans = SpanSet()
        for sensor in self.sensors:
            span = self.get_sensor_slice(sensor, y)
            if span:
                spans.add_span(span)
        beacons = {x[0] for x in self.beacons if x[1] == y}
        return spans.total - len(beacons)

    def find_beacon(self, limit: int) -> tuple:
        region = (-limit, limit, 0, limit + limit)
        regions = {region}
        for sensor in self.sensors:
            rect = get_rect(sensor, self.ranges[sensor])
            regions = subtract_rect(regions, rect)
            logging.debug(regions)

        # Expecting to find exactly one region that contains a single cell.
        singles = tuple(x for x in regions if x[0] == x[1] and x[2] == x[3])
        assert len(singles) == 1

        # Now we have to map the diagonal bounds of the diamond region shape
        # back to an actual cell coordinate.
        remain = next(iter(singles))
        sw = remain[0]
        nw = remain[2]
        x = (sw + nw) // 2
        y = nw - x
        return (x, y)


def parse(stream) -> list:
    result = []
    for line in stream:
        parts = re.findall(r'-?\d+', line)
        sx, sy, bx, by = map(int, parts)
        result.append(((sx, sy), (bx, by)))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        coords = parse(stream)
        grid = Grid()
        grid.load_coords(coords)
        y = 10 if test else 2000000
        result1 = grid.count_possible(y)

    with timing("Part 2"):
        limit = 20 if test else 4000000
        x, y = grid.find_beacon(limit)
        result2 = x * 4000000 + y

    return (result1, result2)
