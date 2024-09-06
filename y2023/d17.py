#!/usr/bin/env python
import heapq
from collections import defaultdict, namedtuple

from util import timing, Direction


VECTORS = {
        Direction.NORTH: (-1,  0),
        Direction.SOUTH:  (1,  0),
        Direction.EAST:   (0,  1),
        Direction.WEST:   (0, -1),
        }
TURNS = {
        # facing direction: (left turn, right turn)
        Direction.EAST: (Direction.NORTH, Direction.SOUTH),
        Direction.WEST: (Direction.SOUTH, Direction.NORTH),
        Direction.NORTH: (Direction.WEST, Direction.EAST),
        Direction.SOUTH: (Direction.EAST, Direction.WEST),
        }


def in_bounds(height: int, width: int, position: tuple[int]) -> bool:
    y, x = position
    return y >= 0 and y < height and x >= 0 and x < width


def move(
        position: tuple[int],
        direction: Direction,
        count: int = 1,
        ) -> tuple[int]:
    v = tuple(x * count for x in VECTORS[direction])
    return (position[0] + v[0], position[1] + v[1])


def get_min_distance(a: tuple[int], b: tuple[int]) -> int:
    if a == b:
        return 0
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


Node = namedtuple('node', ['y', 'x', 'd', 'r'])


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


def get_neighbours(
        node: Node,
        height: int,
        width: int,
        min_run: int = 0,
        max_run: int = 3,
        ) -> list[Node]:
    left, right = TURNS[node.d]
    result = []

    if node.r >= min_run or node.r == 0:
        # Special case for r == 0 because we can move off in either direction
        # from the starting node.
        dist = max(min_run, 1)
        pos = move((node.y, node.x), left, dist)
        if in_bounds(height, width, pos):
            result.append(Node(*pos, left, dist))

        pos = move((node.y, node.x), right, dist)
        if in_bounds(height, width, pos):
            result.append(Node(*pos, right, dist))

        if node.r < max_run:
            pos = move((node.y, node.x), node.d)
            if in_bounds(height, width, pos):
                result.append(Node(*pos, node.d, node.r + 1))
    else:
        # must continue forward until we reach minimum run length
        count = min_run - node.r
        pos = move((node.y, node.x), node.d, count)
        if in_bounds(height, width, pos):
            result.append(Node(*pos, node.d, node.r + count))

    return result


def build_path(origins: dict, end: Node) -> list[Node]:
    result = []
    node = end
    while node in origins:
        node = origins[node]
        result.insert(0, node)
    return result


def get_cost(rows: list, start: Node, end: Node) -> int:
    """Get the total heat cost for straight line travel."""
    pos = (start.y, start.x)
    dest = (end.y, end.x)
    result = 0
    while pos != dest:
        pos = move(pos, end.d)
        result += rows[pos[0]][pos[1]]
    return result


def find_path_astar(rows: list, min_run: int = 0, max_run: int = 3) -> int:
    height = len(rows)
    width = len(rows[0])

    def inf() -> float:
        return float('inf')

    start = Node(0, 0, Direction.EAST, 0)
    dest = Node(height - 1, width - 1, Direction.EAST, 0)
    nodes = PriorityQueue()
    nodes.push(start, get_min_distance(start, dest))
    origins = {}
    g = defaultdict(inf)
    f = defaultdict(inf)
    g[start] = 0

    while nodes:
        heat, current = nodes.pop()
        if current[:2] == dest[:2]:
            return heat

        neighbours = get_neighbours(current, height, width, min_run, max_run)
        for neighbour in neighbours:
            score = g[current] + get_cost(rows, current, neighbour)
            if score < g[neighbour]:
                # Best path to the neighbour so far
                origins[neighbour] = current
                g[neighbour] = score
                dist = get_min_distance(neighbour, dest)
                fscore = score + dist

                f[neighbour] = fscore
                nodes.set_priority(neighbour, fscore)
    print("Ran out of nodes without finding the destination!")


def run(stream, test=False):
    rows = []
    for line in stream:
        rows.append([int(x) for x in line.strip()])

    # Part 1
    with timing("Part 1"):
        score1 = find_path_astar(rows)
    print(f"Result for Part 1 = {score1}\n")

    # Part 2
    with timing("Part 2"):
        score2 = find_path_astar(rows, 4, 10)
    print(f"Result for Part 2 = {score2}\n")
    return (score1, score2)
