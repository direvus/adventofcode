"""Advent of Code 2019

Day 24: Planet of Discord

https://adventofcode.com/2019/day/24
"""
import logging  # noqa: F401

from util import timing


class Grid:
    """A square grid for a Conway's Game of Life ... with bugs!

    I'm doing my part.
    """
    def __init__(self, stream=None, size: int = 5):
        self.size = size
        self.bugs = set()
        if stream:
            self.parse(stream)

    def parse(self, stream):
        if isinstance(stream, str):
            stream = stream.split('\n')
        y = 0
        for line in stream:
            line = line.strip()
            if line == '':
                continue
            for x, ch in enumerate(line):
                if ch == '#':
                    self.bugs.add((x, y))
            y += 1

    def get_adjacents(self, position: tuple) -> set[tuple]:
        x, y = position
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}

    def count_adjacent_bugs(self, position: tuple) -> int:
        return len(self.get_adjacents(position) & self.bugs)

    def update(self):
        new = set()
        for y in range(self.size):
            for x in range(self.size):
                p = (x, y)
                count = self.count_adjacent_bugs(p)
                bug = p in self.bugs
                if count == 1 or (count == 2 and not bug):
                    new.add(p)
        self.bugs = new

    def run_until_repeat(self) -> int:
        configs = set()
        div = self.get_biodiversity()
        while div not in configs:
            configs.add(div)
            self.update()
            div = self.get_biodiversity()
        return div

    def get_biodiversity(self) -> int:
        result = 0
        n = 1
        for y in range(self.size):
            for x in range(self.size):
                p = (x, y)
                if p in self.bugs:
                    logging.debug(f"At {p}, adding {n}")
                    result += n
                n *= 2
        return result


def parse(stream) -> Grid:
    grid = Grid(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.run_until_repeat()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
