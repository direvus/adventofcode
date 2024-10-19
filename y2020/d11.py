"""Advent of Code 2020

Day 11: Seating System

https://adventofcode.com/2020/day/11
"""
import logging  # noqa: F401

from util import timing


VECTORS = {
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)}


class Grid:
    def __init__(self, stream=''):
        self.seats = set()
        self.occupied = set()
        self.adjacent = {}
        self.width = 0
        self.height = 0

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        for line in stream:
            for x, ch in enumerate(line.strip()):
                p = (x, y)
                if ch == 'L':
                    self.seats.add(p)
            y += 1
        self.height = y + 1
        self.width = x + 1

    def get_adjacent(self, position: tuple) -> set[tuple]:
        """Return all of the 8 adjacent squares that are seats."""
        if position in self.adjacent:
            return self.adjacent[position]

        x, y = position
        squares = {
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y), (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
                }
        adj = squares & self.seats
        self.adjacent[position] = adj
        return adj

    def get_occupied_adjacent(self, position: tuple) -> set[tuple]:
        """Return all of the adjacent seats that are occupied."""
        return self.get_adjacent(position) & self.occupied

    def update(self):
        new = set(self.occupied)
        for seat in self.seats:
            adj = self.get_occupied_adjacent(seat)
            count = len(adj)
            if seat in self.occupied and count >= 4:
                new.remove(seat)
            elif seat not in self.occupied and count == 0:
                new.add(seat)
        self.occupied = new

    def run_until_stable(self):
        prev = None
        while self.occupied != prev:
            prev = set(self.occupied)
            self.update()


class GridPart2(Grid):
    def __init__(self, stream=''):
        self.seats = set()
        self.occupied = set()
        self.adjacent = {}

        if stream:
            self.parse(stream)

    def find_first_seat(self, position: tuple, vector: tuple) -> tuple | None:
        """Return the first seat visible from `position`.

        Moving in the direction given by `vector`, return the first seat we
        encounter, or None if we leave the grid without encountering any seat.
        """
        vx, vy = vector
        x, y = position[0] + vx, position[1] + vy
        while x >= 0 and y >= 0 and x < self.width and y < self.height:
            p = (x, y)
            if p in self.seats:
                return p
            x += vx
            y += vy
        return None

    def get_adjacent(self, position: tuple) -> set[tuple]:
        """Return all of the seats that are visible from `position`."""
        if position in self.adjacent:
            return self.adjacent[position]

        adj = set()
        for vector in VECTORS:
            seat = self.find_first_seat(position, vector)
            if seat:
                adj.add(seat)

        self.adjacent[position] = adj
        return adj

    def update(self):
        new = set(self.occupied)
        for seat in self.seats:
            adj = self.get_occupied_adjacent(seat)
            count = len(adj)
            if seat in self.occupied and count >= 5:
                new.remove(seat)
            elif seat not in self.occupied and count == 0:
                new.add(seat)
        self.occupied = new


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        grid.run_until_stable()
        result1 = len(grid.occupied)

    with timing("Part 2"):
        grid2 = GridPart2()
        grid2.seats = grid.seats
        grid2.height = grid.height
        grid2.width = grid.width
        grid2.run_until_stable()
        result2 = len(grid2.occupied)

    return (result1, result2)
