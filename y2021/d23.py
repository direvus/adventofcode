"""Advent of Code 2021

Day 23: Amphipod

https://adventofcode.com/2021/day/23
"""
import logging  # noqa: F401
from collections import defaultdict, deque
from functools import cache

from util import timing, PriorityQueue, INF


COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HOME_COLUMNS = {3: 'A', 5: 'B', 7: 'C', 9: 'D'}
HOME_LETTERS = {v: k for k, v in HOME_COLUMNS.items()}


@cache
def is_home_col_valid(pods, letter) -> bool:
    """Return whether the given home room is valid.

    A home room is valid if it does not contain any amphipods of a different
    letter.
    """
    return not any(pod and pod != letter for pod in pods)


@cache
def get_valid_home_cols(pods) -> set:
    """Return the X-values for valid home rooms.

    Valid home rooms are those that do not contain any amphipods of the
    wrong letter.
    """
    result = set()
    for x, letter in HOME_COLUMNS.items():
        if is_home_col_valid(pods[x - 1], letter):
            result.add(x)
    return result


@cache
def get_home_pods(pods) -> set:
    """Return the positions of pods that are in a final home position.

    A pod is in final home position if it is in the correct room for its
    letter, and there are no pods of a different letter in that same room.
    """
    result = set()
    for x, letter in HOME_COLUMNS.items():
        col = set()
        valid = True
        y = 1
        for pod in pods[x - 1]:
            if pod:
                if pod != letter:
                    valid = False
                    break
                col.add((x, y))
            y += 1
        if valid:
            result |= col
    return result


@cache
def count_home_pods(pods) -> set:
    """Return the number of pods that are in a final home position.

    A pod is in final home position if it is in the correct room for its
    letter, and there are no pods of a different letter in that same room.
    """
    result = 0
    for x, letter in HOME_COLUMNS.items():
        if is_home_col_valid(pods[x - 1], letter):
            result += len(pods[x - 1])
    return result


@cache
def get_positions(pods) -> dict:
    """Return the positions of amphipods in this configuration.

    The result is a dict mapping (x, y) positions to letters. Empty spaces are
    not included in the dict.
    """
    result = {}
    x = 1
    for col in pods:
        y = 1
        for pod in col:
            if pod:
                result[(x, y)] = pod
            y += 1
        x += 1
    return result


@cache
def get_path_heuristic(pods) -> int:
    """Return a path heuristic score for this configuration.

    For each pod that is not home, we calculate a score based on the number of
    steps needed for it to reach the hallway, plus the number of steps to reach
    the first square of its home room, times its movement cost. The possible
    cost of moving deeper into the home room is not taken into account.

    The final result is the sum of these scores.
    """
    valid = get_valid_home_cols(pods)
    result = 0
    x = 1
    for col in pods:
        y = 1
        for pod in col:
            if not pod:
                continue
            home = HOME_LETTERS[pod]
            if x == home and x in valid:
                continue
            steps = 0
            if y > 1:
                steps += 1 + (y - 1)
            if x != home:
                steps += abs(home - x)
            else:
                steps += 2
            result += steps * COSTS[pod]
            y += 1
        x += 1
    return result


def make_node(node, letter, source, dest) -> tuple:
    cols = []
    x = 1
    for pods in node:
        y = 1
        col = []
        for pod in pods:
            p = (x, y)
            if p == dest:
                pod = letter
            elif p == source:
                pod = ''

            col.append(pod)
            y += 1
        cols.append(tuple(col))
        x += 1
    return tuple(cols)


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)


class Grid:
    def __init__(self, stream=''):
        self.spaces = set()
        self.nostop = {(x, 1) for x in HOME_COLUMNS}
        self.rooms = {}
        self.homes = defaultdict(list)
        self.pods = []
        self.home_pod_cache = {}
        self.maxy = 1
        self.maxx = 1

        if stream:
            self.parse(stream)
            self.build_graph()

    def parse(self, stream):
        y = 0
        for line in stream:
            for x, ch in enumerate(line):
                p = (x, y)
                if ch == '#':
                    continue
                elif ch == '.':
                    self.spaces.add(p)
                elif ch in 'ABCD':
                    self.spaces.add(p)
                    self.pods.append((ch, p))

                if y > 1 and x in HOME_COLUMNS:
                    letter = HOME_COLUMNS[x]
                    self.rooms[p] = letter
                    self.homes[letter].append(p)
            y += 1
        self.maxy = y - 2
        self.maxx = x

    def get_adjacent_spaces(self, position):
        x, y = position
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & self.spaces

    def build_graph(self):
        g = Graph()
        for space in self.spaces:
            g.nodes.add(space)
            adjacents = self.get_adjacent_spaces(space)
            for adj in adjacents:
                g.edges[adj].add(space)
                g.edges[space].add(adj)
        self.graph = g

    def find_moves(self, pods, letter, position):
        """Find all possible moves for a pod.

        Return an iterable of moves, where each move is a tuple containing the
        cost of the move and the final position.
        """
        others = get_positions(pods)
        blocked = set(others.keys())
        hallway = position[1] == 1

        # Do a BFS for all possible destinations using basic movement
        # rules, then eliminate destinations that aren't available due to
        # amphipod special rules.
        q = deque()
        q.append((0, position))
        destinations = {}
        explored = {position}
        while q:
            cost, p = q.popleft()
            neighbours = self.graph.edges[p] - blocked - explored
            cost += COSTS[letter]
            for n in neighbours:
                destinations[n] = cost
                q.append((cost, n))
            explored.add(p)
        if not destinations:
            return ()

        col = HOME_LETTERS[letter]
        home_valid = is_home_col_valid(pods[col - 1], letter)
        if hallway:
            # An amphipod starting in the hallway can only move into its home
            # room. And if it is heading for its home room, might as well force
            # it to move as far down into the room as it can go.
            if not home_valid:
                return ()
            y = self.maxy
            while y > 1:
                p = (col, y)
                if not pods[col - 1][y - 1] and p in destinations:
                    return ((destinations[p], p),)
                y -= 1
            return ()

        return tuple(
                (v, k) for k, v in destinations.items()
                if k[1] == 1 and k[0] not in HOME_COLUMNS)

    def find_least_cost(self):
        """Find the way to sort the amphipods for the least cost."""
        # Nodes are structured as a tuple of columns, with each column being a
        # tuple of amphipod letters in that column. Empty positions are
        # represented by the empty string.
        pods = {p: c for c, p in self.pods}
        node = []
        for x in range(1, self.maxx + 1):
            col = []
            maxy = self.maxy if x in HOME_COLUMNS else 1
            for y in range(1, maxy + 1):
                col.append(pods.get((x, y), ''))
            node.append(tuple(col))
        node = tuple(node)

        cost = defaultdict(lambda: INF)
        cost[node] = 0
        q = PriorityQueue()
        q.push(node, 0)
        count = len(self.pods)
        while q:
            priority, node = q.pop()
            spend = cost[node]
            homepods = get_home_pods(node)
            logging.debug(f'{node} with {len(homepods)} home')
            if len(homepods) == count:
                return spend

            x = 1
            for col in node:
                y = 1
                for letter in col:
                    if not letter:
                        y += 1
                        continue

                    p = (x, y)
                    if p in homepods:
                        logging.debug(f'{letter} {p} is already home')
                        break

                    if y == 1 and not is_home_col_valid(node[x - 1], letter):
                        logging.debug(f'{letter} {p} in hallway and home not valid')
                        break

                    moves = self.find_moves(node, letter, p)
                    logging.debug(f'{letter} {p} has moves {moves}')
                    for energy, target in moves:
                        new = make_node(node, letter, p, target)
                        newcost = spend + energy
                        if newcost < cost[new]:
                            cost[new] = newcost
                            h = get_path_heuristic(new)
                            q.set_priority(new, newcost + h)
                    break
                x += 1
        raise ValueError('exhausted move queue without finding a solution')


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_least_cost()

    with timing("Part 2"):
        # Add two extra rows to the starting configuration. First, bump the
        # existing bottom row down 2 rows to make room.
        for i, (letter, space) in enumerate(grid.pods):
            x, y = space
            if y == 3:
                p = (x, y + 2)
                grid.pods[i] = (letter, p)
                roomletter = grid.rooms[space]
                grid.rooms[(x, y + 1)] = roomletter
                grid.rooms[(x, y + 2)] = roomletter
                grid.homes[roomletter].append((x, y + 1))
                grid.homes[roomletter].append((x, y + 2))
        extras = {
                (3, 3): 'D',
                (5, 3): 'C',
                (7, 3): 'B',
                (9, 3): 'A',
                (3, 4): 'D',
                (5, 4): 'B',
                (7, 4): 'A',
                (9, 4): 'C',
                }
        for space, letter in extras.items():
            grid.pods.append((letter, space))
        result2 = grid.find_least_cost()

    return (result1, result2)
