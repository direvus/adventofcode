"""Advent of Code 2020

Day 12: Rain Risk

https://adventofcode.com/2020/day/12
"""
import logging  # noqa: F401

from util import timing


DIRECTIONS = 'NESW'
TURNS = {'L': -1, 'R': 1}
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


class Ship:
    def __init__(self, stream=''):
        self.position = (0, 0)
        self.direction = 1
        self.actions = []

        if stream:
            self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            code = line[0]
            value = int(line[1:])
            self.actions.append((code, value))

    def move(self, direction: int, distance: int):
        x, y = self.position
        vx, vy = VECTORS[direction]
        self.position = (x + vx * distance, y + vy * distance)

    def turn(self, change: int):
        self.direction = (self.direction + change) % 4

    def go_forward(self, distance: int):
        self.move(self.direction, distance)

    def do_action(self, code, value):
        if code in DIRECTIONS:
            index = DIRECTIONS.index(code)
            self.move(index, value)
            return

        if code in TURNS:
            rotations = value // 90
            self.turn(TURNS[code] * rotations)
            return

        if code == 'F':
            self.go_forward(value)
            return

        raise ValueError(f"Unknown action {code}")

    def run(self):
        for code, value in self.actions:
            self.do_action(code, value)

    @property
    def distance_from_origin(self) -> int:
        return abs(self.position[0]) + abs(self.position[1])


class WaypointShip(Ship):
    def __init__(self, stream=''):
        super().__init__(stream)
        self.waypoint = (10, -1)

    def move(self, direction: int, distance: int):
        x, y = self.waypoint
        vx, vy = VECTORS[direction]
        self.waypoint = (x + vx * distance, y + vy * distance)

    def turn(self, change: int):
        change %= 4
        if change == 0:
            return

        x, y = self.waypoint
        match change:
            case 1:
                self.waypoint = (-y, x)
            case 2:
                self.waypoint = (-x, -y)
            case 3:
                self.waypoint = (y, -x)

    def go_forward(self, distance: int):
        x, y = self.position
        vx, vy = self.waypoint
        self.position = (x + vx * distance, y + vy * distance)


def parse(stream) -> Ship:
    return Ship(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        ship = parse(stream)
        ship.run()
        result1 = ship.distance_from_origin

    with timing("Part 2"):
        wayship = WaypointShip()
        wayship.actions = ship.actions
        wayship.run()
        result2 = wayship.distance_from_origin

    return (result1, result2)
