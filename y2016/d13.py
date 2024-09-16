from collections import defaultdict
from functools import cache

from util import PriorityQueue


try:
    from PIL import Image
except ImportError:
    # That's fine, visualisations won't be available though.
    pass


INF = float('inf')
PIXELS = {
        'path': 'assets/green_pixel_4.png',
        'explored': 'assets/orange_pixel_4.png',
        'wall': 'assets/grey_pixel_4.png',
        }


@cache
def is_space(x: int, y: int, magic: int) -> bool:
    n = x ** 2 + 3 * x + 2 * x * y + y + y ** 2 + magic
    ones = sum(1 for x in bin(n) if x == '1')
    return ones % 2 == 0


def get_neighbours(location: tuple, magic: int) -> list:
    """Return a list of valid neighbours of the current location.

    At most there are four possible neighbours for a location: up, down, left
    and right of it. If the x-value is zero, we can't go left, and likewise if
    the y-value is zero, we can't go up. There is no upper limit on x- or y-
    values (the grid continues infinitely in both positive directions).

    Any neighbour that is not a space is excluded.

    The return value is a list of (x, y) tuples.
    """
    x, y = location
    neighbours = [(x + 1, y), (x, y + 1)]
    if x > 0:
        neighbours.append((x - 1, y))
    if y > 0:
        neighbours.append((x, y - 1))

    return [p for p in neighbours if is_space(*p, magic)]


def trace_to_path(trace: dict, end: tuple) -> list:
    result = [end]
    node = end
    while node in trace:
        result.insert(0, trace[node])
        node = trace[node]
    return result


def get_min_distance(a: tuple[int], b: tuple[int]) -> int:
    """Return the Manhattan distance between two points."""
    if a == b:
        return 0
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def find_fewest_moves(
        start: tuple, goal: tuple, magic: int, draw: bool = False) -> int:
    """Find the fewest number of moves needed to reach the goal.

    The `magic` number is applied to `is_space()` to discover which locations
    are traversable.
    """
    trace = {}
    q = PriorityQueue()
    q.push(start, get_min_distance(start, goal))
    dist = defaultdict(lambda: INF)
    dist[start] = 0
    explored = set()
    frames = []

    while q:
        cost, node = q.pop()
        if node == goal:
            if draw:
                path = set(trace_to_path(trace, node))
                frames.append((explored, path))

                maxcoord = max(max(p) for p in explored | path) + 2
                size = 5 * maxcoord + 1  # 4 pixels per cell, plus border

                bg = draw_background(magic, size)

                images = [draw_frame(bg, *f) for f in frames]
                images[0].save(
                        'out/y2016d13p1_astar.gif', save_all=True,
                        append_images=images[1:], duration=100)
            return cost

        if draw:
            frames.append((set(explored), {start, goal}))
        for n in get_neighbours(node, magic):
            score = dist[node] + 1
            if score < dist[n]:
                dist[n] = score
                trace[n] = node
                f = score + get_min_distance(n, goal)
                q.set_priority(n, f)
        explored.add(node)
    raise ValueError("Ran out of moves to try!")


def draw_background(magic: int, size: int):
    im = Image.new('RGB', (size, size), '#1a1a1a')
    wall = Image.open(PIXELS['wall'])
    for i in range(size):
        for j in range(size):
            y = 1 + i * 5
            x = 1 + j * 5
            if not is_space(j, i, magic):
                im.paste(wall, (x, y))
    return im


def draw_frame(bg, explored: set, path: set):
    im = bg.copy()
    pixel = Image.open(PIXELS['explored'])
    for p in explored:
        x = 1 + p[0] * 5
        y = 1 + p[1] * 5
        im.paste(pixel, (x, y))
    pixel = Image.open(PIXELS['path'])
    for p in path:
        x = 1 + p[0] * 5
        y = 1 + p[1] * 5
        im.paste(pixel, (x, y))
    return im


def run(stream, test=False, draw=False):
    magic = int(stream.readline().strip())
    goal = (7, 4) if test else (31, 39)

    result1 = find_fewest_moves((1, 1), goal, magic, draw)
    result2 = 0

    return (result1, result2)
