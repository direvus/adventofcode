import time
from collections import namedtuple
from contextlib import contextmanager
from enum import Enum, auto
from functools import total_ordering


@contextmanager
def timing(message: str = None) -> int:
    start = time.perf_counter_ns()
    if message:
        print(f"[......] {message}", end='')
    try:
        yield start
    finally:
        end = time.perf_counter_ns()
        dur = end - start
        print(f"\r\033[2K[{dur//1000:6d}] {message}")


@total_ordering
class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        if self == Direction.NORTH:
            return 'N'
        if self == Direction.EAST:
            return 'E'
        if self == Direction.WEST:
            return 'W'
        return 'S'


Point = namedtuple('point', ['y', 'x'])


VECTORS = {
        Direction.NORTH: (-1,  0),
        Direction.SOUTH:  (1,  0),
        Direction.EAST:   (0,  1),
        Direction.WEST:   (0, -1),
        }


def move(
        point: Point,
        direction: Direction,
        count: int = 1,
        ) -> Point:
    v = tuple(x * count for x in VECTORS[direction])
    return Point(point[0] + v[0], point[1] + v[1])


def minmax(a, b):
    if a < b:
        return a, b
    return b, a
