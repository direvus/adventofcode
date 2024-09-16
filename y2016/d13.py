from functools import cache


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


def find_fewest_moves(start: tuple, goal: tuple, magic: int) -> int:
    """Find the fewest number of moves needed to reach the goal.

    The `magic` number is applied to `is_space()` to discover which locations
    are traversable.
    """
    explored = {start}
    trace = {}
    q = [(0, start)]

    while q:
        cost, node = q.pop(0)
        if node == goal:
            return cost

        for n in get_neighbours(node, magic):
            if n in explored:
                continue
            explored.add(n)
            trace[n] = node
            q.append((cost + 1, n))
    raise ValueError("Ran out of moves to try!")


def run(stream, test=False, draw=False):
    magic = int(stream.readline().strip())
    goal = (7, 4) if test else (31, 39)

    result1 = find_fewest_moves((1, 1), goal, magic)
    result2 = 0

    return (result1, result2)
