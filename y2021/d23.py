"""Advent of Code 2021

Day 23: Amphipod

https://adventofcode.com/2021/day/23
"""
import logging  # noqa: F401
from collections import defaultdict, deque

from util import timing, PriorityQueue, INF


COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


class Grid:
    def __init__(self, stream=''):
        self.spaces = set()
        self.hallway = set()
        self.nostop = set()
        self.rooms = {}
        self.homes = defaultdict(list)
        self.pods = []
        self.home_pod_cache = {}

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        room_index = {}
        room_letter = ord('A')
        for line in stream:
            for x, ch in enumerate(line):
                p = (x, y)
                if ch == '#':
                    continue
                elif ch == '.':
                    self.spaces.add(p)
                    self.hallway.add(p)
                elif ch in 'ABCD':
                    if x not in room_index:
                        room_index[x] = chr(room_letter)
                        room_letter += 1
                        self.nostop.add((x, y - 1))
                    letter = room_index[x]
                    self.spaces.add(p)
                    self.rooms[p] = letter
                    self.homes[letter].append(p)
                    self.pods.append((ch, p))
            y += 1

    def get_adjacent_spaces(self, position):
        x, y = position
        return {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & self.spaces

    def find_moves(self, pods, letter, position):
        """Find all possible moves for a pod.

        Return an iterable of moves, where each move is a tuple containing the
        cost of the move and the final position.
        """
        others = {p: c for c, p in pods if p != position}
        blocked = set(others.keys())
        hallway = position in self.hallway

        # Do a BFS for all possible destinations using basic movement
        # rules, then eliminate destinations that aren't available due to
        # amphipod special rules.
        q = deque()
        q.append((0, position))
        destinations = {}
        explored = {position}
        while q:
            cost, p = q.popleft()
            neighbours = self.get_adjacent_spaces(p) - blocked - explored
            cost += COSTS[letter]
            for n in neighbours:
                destinations[n] = cost
                q.append((cost, n))
            explored.add(p)
        if not destinations:
            return ()

        home_avail = True
        for space, roomletter in self.rooms.items():
            if roomletter != letter:
                # Amphipods cannot move into another letter's home room
                destinations.pop(space, None)
                continue
            # If there is an amphipod of a different letter in the home
            # room, this amphipod can't go there.
            if home_avail and space in others and others[space] != letter:
                home_avail = False
                if hallway:
                    # If this amphipod is in the hallway, its only valid move
                    # is into its home room. If it can't move into its home
                    # room, then it can't move at all.
                    return ()

        if hallway:
            # An amphipod starting in the hallway can only move into its home
            # room. And if it is heading for its home room, might as well force
            # it to move as far down into the room as it can go.
            homespaces = [p for p in self.homes[letter] if p in destinations]
            if not homespaces:
                return ()
            space = homespaces[-1]
            return ((destinations[space], space),)

        # Amphipods cannot stop on the spaces directly outside of rooms, so
        # eliminate those destinations
        return tuple(
                (v, k) for k, v in destinations.items()
                if k not in self.nostop)

    def get_home_pods(self, pods) -> int:
        """Return the positions of pods that are home.

        Being home means that the pod is in its home room, and there are no
        pods of other types in the same room.
        """
        if pods in self.home_pod_cache:
            return self.home_pod_cache[pods]
        result = set()
        locations = {p: c for c, p in pods}
        invalid = set()
        for space, letter in self.rooms.items():
            if space[0] in invalid:
                continue
            if space in locations:
                if locations[space] == letter:
                    result.add(space)
                else:
                    invalid.add(space[0])
        result = {p for p in result if p[0] not in invalid}
        self.home_pod_cache[pods] = result
        return result

    def find_least_cost(self):
        """Find the way to sort the amphipods for the least cost."""
        q = PriorityQueue()
        node = tuple(self.pods)
        q.push(node, (0, 0))
        count = len(self.pods)
        cost = defaultdict(lambda: INF)
        cost[node] = 0
        while q:
            priority, pods = q.pop()
            spend = cost[pods]
            homepods = self.get_home_pods(pods)
            if len(homepods) == count:
                return spend

            for i, (letter, pos) in enumerate(pods):
                if pos in homepods:
                    # This pod is already home, don't try to move it.
                    continue
                moves = self.find_moves(pods, letter, pos)
                for energy, space in moves:
                    new = list(pods)
                    new[i] = (letter, space)
                    node = tuple(new)

                    newcost = spend + energy
                    if newcost < cost[node]:
                        cost[node] = newcost
                        newhome = len(self.get_home_pods(node))
                        q.set_priority(node, newcost + count - newhome)
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
