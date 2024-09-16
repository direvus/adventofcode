import logging
from collections import defaultdict
from _md5 import md5

from util import PriorityQueue


INF = float('inf')
VECTORS = {
        'D': (1, 0),
        'R': (0, 1),
        'U': (-1, 0),
        'L': (0, -1),
        }


def move(location: tuple, vector: tuple) -> tuple:
    return (location[0] + vector[0], location[1] + vector[1])


def get_neighbours(location: tuple, path: str) -> list:
    """Return a list of valid neighbours of the current location.

    At most there are four possible neighbours for a location: up, down, left
    and right of it. This is bounded by the edges of a 4x4 grid space, and
    possibly bounded further by locked doors.

    The return value is a list of (direction, (x, y)) tuples.
    """
    a = ord('a')
    digest = md5(path.encode('ascii')).hexdigest()[:4]

    y, x = location
    directions = []
    if y < 3 and ord(digest[1]) > a:
        directions.append('D')
    if x < 3 and ord(digest[3]) > a:
        directions.append('R')
    if y > 0 and ord(digest[0]) > a:
        directions.append('U')
    if x > 0 and ord(digest[2]) > a:
        directions.append('L')

    return [(d, move(location, VECTORS[d])) for d in directions]


def get_min_distance(a: tuple[int], b: tuple[int]) -> int:
    """Return the Manhattan distance between two points."""
    if a == b:
        return 0
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def find_shortest_path(start: tuple, goal: tuple, code: str) -> str | None:
    """Find the shortest path that can reach the goal.

    The `code` is prefixed to the path at each location to discover which
    doors are open.

    The result is a string of U, D, L and R directions.
    """
    q = PriorityQueue()
    q.push((start, ''), get_min_distance(start, goal))
    dist = defaultdict(lambda: INF)
    dist[(start, '')] = 0

    while q:
        _, (node, path) = q.pop()
        logging.debug(f"At {node} from {path}")
        if node == goal:
            return path

        for d, n in get_neighbours(node, code + path):
            score = dist[(node, path)] + 1
            if score < dist[n]:
                newpath = path + d
                dist[(n, newpath)] = score
                f = score + get_min_distance(n, goal)
                q.set_priority((n, newpath), f)
    return None


def find_longest_path(start: tuple, goal: tuple, code: str) -> str | None:
    """Find the longest path that can reach the goal.

    The `code` is prefixed to the path at each location to discover which
    doors are open.

    The result is a string of U, D, L and R directions.
    """
    q = []
    q.append((start, ''))
    longest = ''
    explored = set()

    while q:
        (node, path) = q.pop(0)
        if node == goal:
            if len(path) > len(longest):
                longest = path
            continue

        for d, n in get_neighbours(node, code + path):
            newpath = path + d
            if (n, newpath) not in explored:
                q.append((n, newpath))
                explored.add((n, newpath))
    return longest


def run(stream, test=False, draw=False):
    code = stream.readline().strip()
    start = (0, 0)
    goal = (3, 3)

    result1 = find_shortest_path(start, goal, code)
    result2 = len(find_longest_path(start, goal, code))

    return (result1, result2)
