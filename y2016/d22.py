"""Advent of Code 2016

Day 22: Grid Computing

https://adventofcode.com/2016/day/22
"""
import logging  # noqa: F401
import re
from collections import defaultdict, namedtuple
from itertools import permutations

from util import timing, PriorityQueue


INF = float('inf')
PATTERN = re.compile(r'node-x(\d+)-y(\d+)')
Node = namedtuple('node', ['x', 'y', 'size', 'used', 'avail', 'usep'])


class Grid:
    def __init__(self, nodes: dict):
        self.nodes = nodes
        self.width = max(k[0] for k in nodes.keys()) + 1
        self.height = max(k[1] for k in nodes.keys()) + 1
        self.rows = []
        self.empty_node = None
        self.blocked_nodes = set()
        for y in range(self.height):
            row = []
            for x in range(self.width):
                loc = (x, y)
                node = self.nodes[loc]
                row.append(node)
                if node.used == 0:
                    self.empty_node = loc
                elif node.used > 100:
                    self.blocked_nodes.add(loc)
            self.rows.append(row)

    def to_string(self) -> str:
        result = []
        for row in self.rows:
            line = []
            for node in row:
                glyph = '.'
                if node.used == 0:
                    glyph = ' '
                elif node.used > 100:
                    glyph = '#'
                elif node.x == 0 and node.y == 0:
                    glyph = 'H'
                elif node.x == self.width - 1 and node.y == 0:
                    glyph = '*'
                line.append(glyph)
            result.append(''.join(line))
        return '\n'.join(result)

    def get_neighbours(self, pos: tuple) -> set:
        """Get all the valid neighbouring nodes.

        A valid neighbour is one that could move data into the current node,
        assuming the current node were empty. That is, it must be vertically or
        horizontally adjacent, and the amount of data held on the neighbour is
        not greater than the total size of the current node.
        """
        result = set()
        x, y = pos
        node = self.nodes[pos]
        size = node.size
        if x > 0 and self.nodes[(x - 1, y)].used <= size:
            result.add((x - 1, y))
        if y > 0 and self.nodes[(x, y - 1)].used <= size:
            result.add((x, y - 1))
        if x < self.width - 1 and self.nodes[(x + 1, y)].used <= size:
            result.add((x + 1, y))
        if y < self.height - 1 and self.nodes[(x, y + 1)].used <= size:
            result.add((x, y + 1))
        return result


def parse(stream) -> dict:
    result = {}
    for line in stream:
        words = line.strip().split()
        m = PATTERN.search(words[0])
        if not m:
            # Skip header lines
            continue
        x = int(m.group(1))
        y = int(m.group(2))

        # All the sizes are given in T, so ignore the units
        size = int(words[1][:-1])
        used = int(words[2][:-1])
        avail = int(words[3][:-1])
        usep = int(words[4][:-1])

        node = Node(x, y, size, used, avail, usep)
        result[(x, y)] = node
    return result


def get_viable_pairs(nodes: dict) -> tuple:
    result = []
    for a, b in permutations(nodes.values(), 2):
        if a.used > 0 and a.used <= b.avail:
            result.append(((a.x, a.y), (b.x, b.y)))
    return result


def get_min_distance(a: tuple[int], b: tuple[int]) -> int:
    """Return the Manhattan distance between two points."""
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def find_path_cost(grid: Grid, start, goal) -> int:
    q = PriorityQueue()
    q.push(start, get_min_distance(start, goal))
    dist = defaultdict(lambda: INF)
    dist[start] = 0

    while q:
        cost, node = q.pop()
        if node == goal:
            return cost

        for n in grid.get_neighbours(node):
            score = dist[node] + 1
            if score < dist[n]:
                dist[n] = score
                f = score + get_min_distance(n, goal)
                q.set_priority(n, f)
    raise ValueError("Ran out of moves to try!")


def find_data_move_cost(grid: Grid) -> int:
    """Find the fewest number of moves needed move the data to the home node.

    The data starts out in the top-right corner, and the home node is in the
    top-left corner.

    There is an empty node located somewhere in the grid, and several 'blocked'
    nodes that hold so much data that they can't be used.
    as unusable.

    First we calculate the length of the path from the empty node, to the node
    immediately left of the data node. Then we add the cost of moving the data
    left to the home node by progressively sliding data into the empty node.
    """
    start = grid.empty_node
    goal = (grid.width - 2, 0)
    cost = find_path_cost(grid, start, goal)
    logging.debug(f"Found {cost} move path to prep the empty space")
    cost += 1  # Moving the data left the first time.

    # Now we have this kind of configuration in the top-right corner:
    #
    #    ..*_
    #    ....
    #
    # Moving the data left will cost us 5 steps each time, so just multiply the
    # distance from the current position to the home node by 5, and add that to
    # the cost.
    cost += 5 * get_min_distance(goal, (0, 0))
    return cost


def run(stream, test: bool = False):
    nodes = parse(stream)
    logging.debug(f"Parsed {len(nodes)} nodes")
    grid = Grid(nodes)

    with timing("Part 1"):
        result1 = len(get_viable_pairs(nodes))
    with timing("Part 2"):
        result2 = find_data_move_cost(grid)

    return (result1, result2)
