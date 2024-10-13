"""Advent of Code 2019

Day 19: Tractor Beam

https://adventofcode.com/2019/day/19
"""
import logging  # noqa: F401

from util import timing
from y2019.intcode import Computer


class Grid:
    def __init__(self, program=None):
        self.hits = set()
        self.misses = set()
        self.left = (0, 0)
        self.right = (0, 0)
        self.computer = Computer()
        if program:
            self.computer.parse(program)

    def query(self, position: tuple) -> int:
        if position in self.hits:
            return 1
        elif position in self.misses:
            return 0

        self.computer.reset()
        self.computer.add_inputs(position)
        value = next(self.computer.generate())
        if value:
            self.hits.add(position)
        else:
            self.misses.add(position)
        return value

    def scan(self, minx: int, miny: int, maxx: int, maxy: int) -> int:
        result = 0
        for y in range(50):
            left = None
            right = None
            for x in range(50):
                value = self.query((x, y))
                result += value
                if value:
                    if left is None:
                        left = x
                    right = x
            if value == 0 and left is not None:
                self.width = right - left + 1
                self.centre = left + self.width // 2
                self.distance = y
        return result

    def get_beam_slice(self, y: int) -> tuple:
        """Return a horizontal slice of the beam at the Y-value.

        The result is a tuple containing the left edge and right edge of the
        beam at this Y-value, as X-values.
        """
        # Based on our furthest known beam center point, try to project where
        # the center of the beam will be at our desired Y value.
        x = round(y * self.centre / self.distance)
        c = (x, y)
        value = self.query(c)
        if not value:
            # Well this is awkward
            raise ValueError(f"Did not hit the beam at {c}!")
        # Now scan left until we find the left edge of the beam
        left = x
        while value:
            x -= 1
            value = self.query((x, y))
            if value:
                left = x

        # And then right from the centre until we find the right edge
        x = c[0]
        value = True
        right = x
        while value:
            x += 1
            value = self.query((x, y))
            if value:
                right = x

        return left, right

    def get_beam_width(self, y: int) -> int:
        left, right = self.get_beam_slice(y)
        return right - left + 1

    def find_square_x(self, size: int, y: int) -> int | None:
        """Return where the square can fit within this Y-value.

        The result is either the X-value of the top left corner of the fit box,
        or None if the square cannot fit here.
        """
        # Find the right edge of the beam at this position, move left from
        # there to accomodate the square horizontally, and test whether it fits
        # in the vertical there too.
        left, right = self.get_beam_slice(y)
        width = right - left + 1
        if width < size:
            # Well that's an easy answer
            return None
        x = right - size + 1
        for i in range(y, y + size):
            if not self.query((x, i)):
                return None
        return x

    def find_square_fit(self, size: int) -> tuple:
        """Find the closest position that can fit this square.

        The result is the top left corner of the box where this square can fit
        entirely within the beam, closest to the beam emitter.
        """
        # Use a bisecting search to find the place where the beam can fit the
        # square.
        low = 0
        high = size * 10
        diff = high - low

        while diff > 1:
            x = self.find_square_x(size, high)
            diff = (high - low) // 2
            if x is None:
                low = high
            high = low + diff

        # Now test whether the square can fit at this position. If it can, move
        # up until it doesn't fit anymore and return the last successful
        # location. If it doesn't, move down until it does fit and return the
        # first successful.
        y = high
        x = self.find_square_x(size, y)

        fit = x
        if x is not None:
            while fit is not None:
                y -= 1
                fit = self.find_square_x(size, y)
                if fit is not None:
                    x = fit
                logging.debug(f"Fit at Y = {y} is {fit}")
            y += 1
        else:
            while fit is None:
                y += 1
                fit = self.find_square_x(size, y)
                if fit is not None:
                    x = fit
                logging.debug(f"Fit at Y = {y} is {fit}")
        return (x, y)

    def to_string(self, minx: int, miny: int, maxx: int, maxy: int) -> str:
        lines = []
        for y in range(miny, maxy + 1):
            line = []
            for x in range(minx, maxx + 1):
                p = (x, y)
                ch = '#' if p in self.hits else (
                        '.' if p in self.misses else ' ')
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> Grid:
    return Grid(stream.readline().strip())


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.scan(0, 0, 50, 50)
        print(grid.to_string(0, 0, 50, 50))

    with timing("Part 2"):
        x, y = grid.find_square_fit(100)
        result2 = x * 10000 + y

    return (result1, result2)
