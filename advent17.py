#!/usr/bin/env python
import heapq
import sys
from collections import defaultdict, namedtuple
from functools import cache

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


@cache
def in_bounds(height: int, width: int, position: tuple[int]) -> bool:
    y, x = position
    return y >= 0 and y < height and x >= 0 and x < width


def move(position: tuple[int], direction: Direction) -> tuple[int]:
    v = VECTORS[direction]
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


def get_neighbours(node: Node, height: int, width: int) -> list[Node]:
    left, right = TURNS[node.d]
    result = []

    pos = move((node.y, node.x), left)
    if in_bounds(height, width, pos):
        result.append(Node(*pos, left, 1))

    pos = move((node.y, node.x), right)
    if in_bounds(height, width, pos):
        result.append(Node(*pos, right, 1))

    if node.r < 3:
        pos = move((node.y, node.x), node.d)
        if in_bounds(height, width, pos):
            result.append(Node(*pos, node.d, node.r + 1))
    return result


def build_path(origins: dict, end: Node) -> list[Node]:
    result = []
    node = end
    while node in origins:
        node = origins[node]
        result.insert(0, node)
    return result


def find_path_astar(rows: list) -> int:
    height = len(rows)
    width = len(rows[0])

    def inf() -> float:
        return float('inf')

    start = Node(0, 0, Direction.EAST, 0)
    dest = Node(height - 1, width - 1, Direction.EAST, 0)
    nodes = PriorityQueue()
    nodes.push(start, 0)
    origins = {}
    g = defaultdict(inf)
    f = defaultdict(inf)
    g[start] = 0
    f[start] = get_min_distance(start, dest)

    while nodes:
        heat, current = nodes.pop()
        if current[:2] == dest and not nodes.has_position(dest):
            return heat

        neighbours = get_neighbours(current, height, width)
        for neighbour in neighbours:
            score = g[current] + rows[neighbour.y][neighbour.x]
            if score < g[neighbour]:
                # Best path to the neighbour so far
                origins[neighbour] = current
                g[neighbour] = score
                fscore = score + get_min_distance(neighbour, dest)
                f[neighbour] = fscore
                nodes.set_priority(neighbour, fscore)


def find_path(rows: list) -> int:
    pos = (0, 0)
    height = len(rows)
    width = len(rows[0])
    direction = Direction.EAST
    nodes = {
            (y, x, d, r): None
            for y in range(height)
            for x in range(width)
            for d in Direction
            for r in range(1, 4)
            if (y, x) != (0, 0)}
    nodes[(0, 0, direction, 0)] = 0
    dest = (height - 1, width - 1)
    run = 0
    heat = 0

    visited = {}

    while [k for k, v in nodes.items() if k[:2] == dest and v is None]:
        left, right = TURNS[direction]
        nbors = [
            (*move(pos, left), left, 1),
            (*move(pos, right), right, 1),
            ]

        if run < 3:
            nbors.append((*move(pos, direction), direction, run + 1))

        nbors = filter(lambda x: x in nodes, nbors)
        for y, x, d, r in nbors:
            dist = nodes[(y, x, d, r)]
            tile = rows[y][x]
            new = heat + tile
            if dist is None or dist > new:
                nodes[(y, x, d, r)] = new

        # DEBUG save off visited for viewing later
        visited[(*pos, direction, run)] = heat
        del nodes[(*pos, direction, run)]

        candidates = [
                (*k, v) for k, v in nodes.items()
                if v is not None]
        if not candidates:
            print("All nodes checked")
            break
        candidates.sort(key=lambda x: x[4])
        y, x, direction, run, heat = candidates[0]
        pos = (y, x)

    heats = [v for k, v in visited.items() if k[:2] == dest and v is not None]
    return min(heats)


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        rows.append([int(x) for x in line.strip()])

    # Part 1
    with timing("Part 1\n"):
        score = find_path_astar(rows)
    print(f"Result for Part 1 = {score}\n")
