import math
import re
from collections import defaultdict
from functools import cache
from itertools import combinations

from util import PriorityQueue


INF = float('inf')
PATTERN = re.compile(r'(\w+)(?:-compatible)? (microchip|generator)')


def parse(stream) -> tuple:
    floors = []
    elements = {}
    e = 0
    for line in stream:
        line = line.strip()
        matches = PATTERN.findall(line)
        items = set()
        for element, function in matches:
            if element not in elements:
                elements[element] = e
                e += 1
            gen = 1 if function == 'generator' else 0
            items.add((elements[element], gen))
        floors.append(items)
    return (0, tuple(frozenset(x) for x in floors))


def get_moves(facility: tuple) -> list:
    """Return a list of valid moves from the current situation.

    The elevator can move up or down one floor at a time, and must carry
    either one or two items.

    Moves that are unsafe (would fry a microchip) will not be returned.

    The result is a list of tuples, where each tuple is in the format
    (move, load). 'move' is either 1, to move up, or -1, to move down, and
    the load is a set of items to bring along.
    """
    moves = []
    loads = []
    elevator, floors = facility
    floor = floors[elevator]
    # Consider single-item loads
    for item in floor:
        load = {item}
        # Is it safe to remove this item from here?
        if is_safe(floor - load):
            loads.append(load)
    # Consider all possible two-item loads
    for com in combinations(floor, 2):
        load = set(com)
        # Is it safe to remove these two items from here?
        if is_safe(floor - load):
            loads.append(set(com))

    targets = []
    if elevator > 0:
        targets.append(-1)
    if elevator < len(floors) - 1:
        targets.append(1)

    for move in targets:
        target = floors[elevator + move]
        for load in loads:
            # Is it safe to bring this load on to this floor?
            if is_safe(target | load):
                moves.append((move, load))
    return moves


def apply_move(facility: tuple, move: int, load: set) -> tuple:
    """Return a new tuple by moving items from one floor to another."""
    elevator, floors = facility
    floors = list(floors)
    floors[elevator] -= load
    elevator += move
    floors[elevator] |= load
    return (elevator, tuple(frozenset(x) for x in floors))


@cache
def is_safe(items: set) -> bool:
    """Return whether the given items are safe to be on the same floor.

    A microchip that is not connected to its matching generator is unshielded.
    An unshielded microchip may not be present on the same floor as any
    generator.
    """
    chips = set()
    generators = set()

    for element, generator in items:
        if generator:
            generators.add(element)
        else:
            chips.add(element)
    unshielded = chips - generators
    return not (unshielded and generators)


def get_min_distance(start: tuple) -> int:
    """Return the fewest conceivable number of moves to reach the goal.

    This is intended for use as a search heuristic, so it only considers the
    ideal case where every move is valid. For each floor below the top floor,
    we look at the number of items, divde by two (because the elevator can
    transport two items at a time), multiply that by the distance to the top
    floor, and finally sum it all together.
    """
    result = 0
    size = len(start[1])
    for i in range(size - 1):
        floor = start[1][i]
        num = math.ceil(len(floor) / 2)
        result += num * (size - 1 - i)
    return result


def find_fewest_moves(start: tuple) -> int:
    """Find the fewest number of moves needed to reach the goal.

    The goal is to have all components safely located on the top floor of the
    facility.
    """
    dist = defaultdict(lambda: INF)
    dist[start] = 0
    q = PriorityQueue()
    q.push(start, 0)

    while q:
        _, node = q.pop()
        if sum(len(x) for x in node[1][:-1]) == 0:
            # Nothing on any floors except the last one, that's a bingo.
            return dist[node]

        for move in get_moves(node):
            neighbour = apply_move(node, *move)
            score = dist[node] + 1
            if score < dist[neighbour]:
                # Best path to that neighbour so far
                dist[neighbour] = score
                fscore = score + get_min_distance(neighbour)
                q.set_priority(neighbour, fscore)
    raise ValueError("Ran out of moves to try!")


def run(stream, test=False, draw=False):
    facility = parse(stream)

    result1 = find_fewest_moves(facility)

    newitems = {('e', 1), ('e', 0)}
    if not test:
        # Adding these last two items breaks the test case
        newitems |= {('d', 1), ('d', 0)}
    floors = (facility[1][0] | newitems,) + facility[1][1:]
    facility2 = (0, tuple(frozenset(x) for x in floors))
    result2 = find_fewest_moves(facility2)

    return (result1, result2)
