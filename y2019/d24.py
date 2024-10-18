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


class NestedGrid(Grid):
    """It's like a Grid, but nested.

    Tiles are represented with 3-tuples that contain the X ordinate, the Y
    ordinate, and the depth level of the tile. The initial state is at depth
    level 0.

    The rules for adjacency are pretty weird, but otherwise the rules for
    propagating bugs are the same as for a Grid.
    """
    def __init__(self, stream=None, size: int = 5):
        super().__init__(stream, size)
        self.mindepth = 0
        self.maxdepth = 0

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
                    self.bugs.add((x, y, 0))
            y += 1

    def get_adjacents(self, position: tuple) -> set[tuple]:
        """Return all the adjacent tiles to this position.

        This is where things get weird in a NestedGrid. If the tile is on an
        edge of the local grid, then it is adjacent to a tile on the next level
        "up". If it's on a corner, then it is adjacent to two tiles on the next
        level "up". If it's adjacent to the centre tile of its local level,
        then instead of including the centre tile, we include five tiles from
        the nearest row or column of the next level "down".
        """
        x, y, d = position
        centre = (2, 2, d)
        result = set()
        if position == centre:
            # The centre position itself doesn't exist as a tile
            return result

        if x > 0:
            result.add((x - 1, y, d))
        else:
            result.add((1, 2, d - 1))

        if y > 0:
            result.add((x, y - 1, d))
        else:
            result.add((2, 1, d - 1))

        if x < self.size - 1:
            result.add((x + 1, y, d))
        else:
            result.add((3, 2, d - 1))

        if y < self.size - 1:
            result.add((x, y + 1, d))
        else:
            result.add((2, 3, d - 1))

        if centre in result:
            result.remove(centre)
            if x == 1:
                result |= {(0, i, d + 1) for i in range(self.size)}
            if x == 3:
                result |= {(self.size - 1, i, d + 1) for i in range(self.size)}
            if y == 1:
                result |= {(i, 0, d + 1) for i in range(self.size)}
            if y == 3:
                result |= {(i, self.size - 1, d + 1) for i in range(self.size)}
        return result

    def count_adjacent_bugs(self, position: tuple) -> int:
        return len(self.get_adjacents(position) & self.bugs)

    def update(self):
        new = set()
        for d in range(self.mindepth - 1, self.maxdepth + 2):
            for y in range(self.size):
                for x in range(self.size):
                    p = (x, y, d)
                    count = self.count_adjacent_bugs(p)
                    bug = p in self.bugs
                    if count == 1 or (count == 2 and not bug):
                        new.add(p)
                        if d < self.mindepth:
                            self.mindepth = d
                        if d > self.maxdepth:
                            self.maxdepth = d
        self.bugs = new

    def run(self, count: int):
        for _ in range(count):
            self.update()

    def run_until_repeat(self) -> int:
        configs = set()
        div = self.get_biodiversity()
        while div not in configs:
            configs.add(div)
            self.update()
            div = self.get_biodiversity()
        return div

    def count_bugs(self) -> int:
        return len(self.bugs)

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

    def to_string(self, depth: int) -> str:
        lines = []
        for y in range(self.size):
            line = []
            for x in range(self.size):
                p = (x, y, depth)
                line.append('#' if p in self.bugs else '.')
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> Grid:
    grid = Grid(stream)
    return grid


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        bugs = frozenset(grid.bugs)
        result1 = grid.run_until_repeat()

    with timing("Part 2"):
        grid = NestedGrid()
        grid.bugs = {(x, y, 0) for x, y in bugs}
        grid.run(200)
        result2 = grid.count_bugs()

    return (result1, result2)
