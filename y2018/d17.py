"""Advent of Code 2018

Day 17: Reservoir Research

https://adventofcode.com/2018/day/17
"""
import logging  # noqa: F401

from util import timing, INF


class Grid:
    def __init__(self):
        self.source = (500, 0)
        self.clay = set()
        self.fill = set()
        self.flow = set()
        self.miny = INF
        self.maxy = 0

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            if line == '':
                break
            parts = line.split(', ')
            fixed, value = parts[0].split('=')
            value = int(value)
            ranged = parts[1].split('=')[1]
            low, high = (int(x) for x in ranged.split('..'))

            if fixed == 'x':
                x = value
                for y in range(low, high + 1):
                    self.clay.add((x, y))
                if high > self.maxy:
                    self.maxy = high
                if low < self.miny:
                    self.miny = low
            else:
                y = value
                if y > self.maxy:
                    self.maxy = y
                if y < self.miny:
                    self.miny = y
                for x in range(low, high + 1):
                    self.clay.add((x, y))

    def do_horizontal_flow(
            self, start: tuple, direction: 1 | -1) -> tuple:
        """Flow water along a horizontal surface.

        The water will flow until there is nothing below it, and it falls, or
        it hits an obstacle, and stops.

        Return a tuple containing the squares traversed, followed by a boolean
        indicating whether the water falls (True) or stops (False).
        """
        x, y = start
        result = []
        while True:
            x += direction
            if (x, y) in self.clay:
                # Stop
                return (result, False)
            self.flow.add((x, y))
            if (x, y + 1) not in self.clay | self.fill:
                # Fall
                result.append((x, y))
                return (result, True)
            result.append((x, y))

    def do_flow(self):
        """Flow water until it leaves the grid.

        Water begins flowing from the source, and initially falls downward
        until it hits an obstacle. Then it flows horizontally in both
        directions. If either direction reaches a square that has nothing
        beneath it, it falls downward again. Otherwise, if both directions hit
        an obstacle, then those squares fill, we move up one Y-level and flow
        out horizontally again.

        If water drops below the maximum Y-level, or rises above the minimum,
        we stop tracking that flow.
        """
        q = [self.source]
        while q:
            x, y = q.pop()
            if y + 1 > self.maxy:
                # Abandon this flow.
                continue
            new = (x, y + 1)
            if new in self.flow:
                # We already have flow here, drop it.
                continue
            if new in (self.clay | self.fill):
                # Encountered a surface, split horizontally.
                lsquares, lfall = self.do_horizontal_flow((x, y), -1)
                rsquares, rfall = self.do_horizontal_flow((x, y), 1)
                if not lfall and not rfall:
                    # Fill
                    squares = set(lsquares) | set(rsquares) | {(x, y)}
                    self.fill |= squares
                    self.flow -= squares
                    self.flow.add((x, y - 1))
                    q.append((x, y - 1))
                if lfall:
                    q.append(lsquares[-1])
                if rfall:
                    q.append(rsquares[-1])
            else:
                # Empty space, continue falling.
                if y + 1 >= self.miny:
                    self.flow.add(new)
                q.append(new)

    def count_water(self) -> int:
        """Return the total number of cells that have water."""
        return len(self.fill | self.flow)

    def count_fill(self) -> int:
        """Return the total number of cells that have filled water."""
        return len(self.fill)

    def to_string(self) -> str:
        result = []
        xs = {x for x, y in self.clay | self.flow | self.fill}
        minx = min(xs)
        maxx = max(xs)
        for y in range(self.miny, self.maxy + 1):
            cells = []
            for x in range(minx, maxx + 1):
                p = (x, y)
                if p in self.clay:
                    ch = '#'
                elif p in self.fill:
                    ch = '~'
                elif p in self.flow:
                    ch = '|'
                else:
                    ch = ' '
                cells.append(ch)
            line = ''.join(cells)
            if '| |' in line:
                logging.debug("Gap at {y}")
            result.append(line)
        return '\n'.join(result) + '\n'


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        grid.do_flow()
        result1 = grid.count_water()

    with timing("Part 2"):
        result2 = grid.count_fill()

    return (result1, result2)
