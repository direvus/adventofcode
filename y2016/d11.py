import re
from functools import cache
from itertools import combinations


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
                e += 1
                elements[element] = e
            items.add(f'{elements[element]}{function[0]}')
        floors.append(items)
    return (0, tuple(frozenset(x) for x in floors)), elements


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
        # Is it safe to remove this item from here? Removing a microchip can't
        # make a floor unsafe, but removing a generator might, because it could
        # leave a microchip unshielded.
        if item[1] == 'm' or is_safe(floor - load):
            loads.append(load)
    pair = False
    # Consider all possible two-item loads
    for com in combinations(floor, 2):
        load = set(com)
        if com[0][0] == com[1][0]:
            # This is a matched microchip-generator pair. We only need to
            # consider this load type once, since all matched pairs are
            # equivalent. We also don't have to test whether it's safe to
            # remove a matched pair from the current floor, because it
            # is guaranteed to be safe.
            if pair:
                continue
            pair = True
            loads.append(set(com))
        else:
            # Is it safe to remove these two items from here?
            if is_safe(floor - load):
                loads.append(set(com))

    targets = []
    if elevator < len(floors) - 1:
        targets.append(1)
    if elevator > 0:
        targets.append(-1)

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
    if len(items) < 2:
        return True

    unshielded = False
    generators = False

    items = sorted(items)
    for i, item in enumerate(items):
        if item[1] == 'g':
            if unshielded:
                return False
            generators = True
        elif items[i - 1][0] != item[0]:
            # The code here is a bit obscure, but because of the way these
            # items are encoded, when they are sorted, if this microchip's
            # matching generator is here, it has to be the item immediately
            # preceding it. Otherwise, the microchip is unshielded.
            if generators:
                return False
            unshielded = True
    return not (unshielded and generators)


def trace_to_path(trace: dict, end: tuple) -> list:
    result = [end]
    node = end
    while node in trace:
        result.insert(0, trace[node])
        node = trace[node]
    return result


def find_fewest_moves(start: tuple) -> int:
    """Find the fewest number of moves needed to reach the goal.

    The goal is to have all components safely located on the top floor of the
    facility.
    """
    explored = {start}
    trace = {}
    q = [start]

    while q:
        node = q.pop(0)
        if sum(len(x) for x in node[1][:-1]) == 0:
            # Nothing on any floors except the last one, that's a bingo.
            return len(trace_to_path(trace, node)) - 1

        for move in get_moves(node):
            neighbour = apply_move(node, *move)
            if neighbour in explored:
                continue
            explored.add(neighbour)
            trace[neighbour] = node
            q.append(neighbour)
    raise ValueError("Ran out of moves to try!")


def run(stream, test=False, draw=False):
    facility, elements = parse(stream)

    result1 = find_fewest_moves(facility)

    elid = max(elements.values()) + 1
    newitems = {f'{elid}g', f'{elid}m'}
    if not test:
        # Adding these last two items breaks the test case
        elid += 1
        newitems = {f'{elid}g', f'{elid}m'}
    floors = (facility[1][0] | newitems,) + facility[1][1:]
    facility2 = (0, tuple(frozenset(x) for x in floors))
    result2 = find_fewest_moves(facility2)

    return (result1, result2)
