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
        self.rooms = defaultdict(set)
        self.pods = []

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
                    self.rooms[letter].add(p)
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
        # Do a BFS search for all possible destinations using basic movement
        # rules, then eliminate destinations that aren't available due to
        # amphipod special rules.
        q = deque()
        q.append((0, position))
        destinations = {}
        while q:
            cost, p = q.popleft()
            if cost > 0:
                destinations[p] = cost
            neighbours = self.get_adjacent_spaces(p) - blocked
            neighbours -= set(destinations.keys())
            cost += COSTS[letter]
            for n in neighbours:
                q.append((cost, n))
        if not destinations:
            return ()

        home = True
        for roomletter, spaces in self.rooms.items():
            for p in spaces:
                if roomletter != letter:
                    # Amphipods cannot move into rooms belonging to other
                    # letters
                    destinations.pop(p, None)
                else:
                    # If there is an amphipod of a different letter in the home
                    # room, this amphipod can't go there.
                    if p in others and others[p] != letter:
                        home = False

        # If this amphipod is in the hallway, its only valid move is into its
        # home room. If it can't move into its home room (i.e., because there
        # is another kind of amphipod in there), then it can't move at all.
        if position in self.hallway:
            if not home:
                return ()
            # If it's heading for its home room, might as well force it to move
            # as far down into the room as it can go.
            homeroom = list(self.rooms[letter] & set(destinations.keys()))
            if not homeroom:
                return ()
            homeroom.sort(reverse=True)
            homespace = homeroom[0]
            return ((destinations[homespace], homespace),)

        # Amphipods cannot stop on the spaces directly outside of rooms, so
        # eliminate those destinations
        for p in self.nostop:
            destinations.pop(p, None)

        return tuple((v, k) for k, v in destinations.items())

    def get_home_pods(self, pods) -> int:
        """Return the positions of pods that are home.

        Being home means that the pod is in its home room, and there are no
        pods of other types in the same room.
        """
        result = set()
        for letter, space in pods:
            room = self.rooms[letter]
            if space in room:
                others = {p for c, p in pods if p in room and c != letter}
                if not others:
                    result.add(space)
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
        logging.debug(vars(grid))
        result1 = grid.find_least_cost()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
