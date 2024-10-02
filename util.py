import heapq
import logging
import time
from collections import namedtuple
from contextlib import contextmanager
from enum import Enum, auto
from functools import total_ordering

try:
    import numba
    jit = numba.jit
except ImportError:
    # Degrade to a no-op decorator if jit isn't available.
    def jit(*args):
        def dec(fn):
            return fn
        return dec


@contextmanager
def timing(message: str = None) -> int:
    start = time.perf_counter_ns()
    if message:
        logging.info(f"[.........] :green_circle: [green]START[/] {message}")
    try:
        yield start
    finally:
        end = time.perf_counter_ns()
        dur = end - start
        micros = dur // 1000
        if micros < 10_000_000:
            t = f'{micros:,d}'
        else:
            seconds = micros / 1_000_000
            t = f'{seconds:,.2f}s'
        logging.info(f"[{t:>9s}] :stop_sign:   [red]END[/] {message}")


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


INF = float('inf')
NINF = float('-inf')


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


def get_manhattan_distance(a: tuple[int], b: tuple[int]) -> int:
    """Return the Manhattan distance between two points."""
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.finder = {}
        self.deleted = set()

    def __len__(self):
        return len(self.queue)

    def __bool__(self):
        return bool(self.finder)

    def push(self, node, priority):
        entry = (priority, node)
        heapq.heappush(self.queue, entry)
        self.finder[node] = entry

    def has_node(self, node):
        return node in self.finder

    def has_position(self, position):
        return position in {(n.y, n.x) for n in self.finder.keys()}

    def set_priority(self, node, priority):
        if node in self.finder:
            self.deleted.add(id(self.finder[node]))
        self.push(node, priority)

    def pop(self):
        while self.queue:
            entry = heapq.heappop(self.queue)
            if id(entry) not in self.deleted:
                del self.finder[entry[1]]
                return entry
            self.deleted.discard(id(entry))
        raise KeyError('Cannot pop from empty priority queue')


@jit
def is_prime(value: int) -> bool:
    for n in range(2, value ** 0.5 + 1):
        if value % n == 0:
            return False
    return True


@jit
def get_divisors(value: int) -> set:
    result = {1, value}
    for n in range(2, value ** 0.5 + 1):
        div, mod = divmod(value, n)
        if mod == 0:
            result.add(div)
            result.add(n)
    return result


def get_digits(value: int) -> tuple:
    digits = []
    if value == 0:
        return (0,)
    while value > 0:
        value, mod = divmod(value, 10)
        digits.append(mod)
    return tuple(reversed(digits))
