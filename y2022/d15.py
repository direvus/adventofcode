"""Advent of Code 2022

Day 15: Beacon Exclusion Zone

https://adventofcode.com/2022/day/15
"""
import logging  # noqa: F401
import re

from spans import SpanSet
from util import get_manhattan_distance, timing


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
        space = SpanSet()
        space.add_span((0, limit))
        for y in range(0, limit):
            spans = SpanSet()
            for sensor in self.sensors:
                span = self.get_sensor_slice(sensor, y)
                spans.add_span(span)
            remain = space - spans
            if remain:
                values = remain.values
                return (next(iter(values)), y)


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
