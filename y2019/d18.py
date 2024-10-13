"""Advent of Code 2019

Day 18: Many-Worlds Interpretation

https://adventofcode.com/2019/day/18
"""
import logging  # noqa: F401
import string
from collections import defaultdict

from util import INF, PriorityQueue, get_manhattan_distance, timing


DIRECTIONS = '^>v<'
VECTORS = ((0, -1), (1, 0), (0, 1), (-1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)


class Grid:
    def __init__(self, stream):
        self.spaces = set()
        self.start = (0, 0)
        self.keys = {}
        self.doors = {}
        self.graph = Graph()

        if stream:
            self.parse(stream)

    def parse(self, stream):
        y = 0
        if isinstance(stream, str):
            stream = stream.split('\n')
        for line in stream:
            line = line.strip()
            if not line:
                continue
            for x, ch in enumerate(line):
                p = (x, y)
                if ch != '#':
                    self.spaces.add(p)

                if ch == '@':
                    self.start = p
                elif ch in string.ascii_lowercase:
                    self.keys[ch] = p
                elif ch in string.ascii_uppercase:
                    self.doors[ch.lower()] = p
            y += 1
        self.make_graph()

    def get_adjacent(self, position: tuple) -> set:
        return {move(position, d) for d in range(len(DIRECTIONS))}

    def make_graph(self):
        """Assemble a graph of the grid space.

        Each square that is an intersection, door, or key will become a node in
        the graph, and linear paths between nodes will become edges.
        """
        graph = Graph()
        pos = self.start
        graph.nodes.add(pos)
        explored = set()
        q = [(pos, 0, pos)]
        doors = set(self.doors.values())
        keys = set(self.keys.values())
        essentials = {self.start} | doors | keys
        while q:
            pos, cost, start = q.pop(0)
            adjacent = self.get_adjacent(pos) & self.spaces - explored
            if len(adjacent) > 1 or pos in essentials:
                graph.nodes.add(pos)
                if cost > 0:
                    graph.edges[start][pos] = cost
                    graph.edges[pos][start] = cost
                cost = 0
                start = pos
            for adj in adjacent:
                q.append((adj, cost + 1, start))
            explored.add(pos)
        self.graph = graph

        # Simplify by removing nodes that only connect between two other nodes.
        # This happens when a position initially looks like an intersection,
        # but further exploration proves some of the branches to be dead ends.
        removable = [
                (k, v) for k, v in graph.edges.items()
                if len(v) == 2 and k not in essentials]
        while removable:
            for node, edges in removable:
                graph.nodes.discard(node)
                graph.edges.pop(node, None)
                others = tuple(edges.keys())
                cost = sum(edges.values())
                for other in others:
                    graph.edges[other].pop(node, None)
                a, b = others
                graph.edges[a][b] = cost
                graph.edges[b][a] = cost
            removable = [
                    (k, v) for k, v in graph.edges.items()
                    if len(v) == 2 and k not in essentials]

    def get_neighbours(self, position: tuple, keys: set) -> dict:
        neighbours = self.graph.edges[position]
        locked = {v for k, v in self.doors.items() if k not in keys}
        return {k: v for k, v in neighbours.items() if k not in locked}

    def find_all_keys_path(self) -> int:
        """Return the fewest steps in which we can gather all keys."""
        q = PriorityQueue()
        q.push((frozenset(), self.start), 0)
        target = len(self.keys)
        keynodes = {v: k for k, v in self.keys.items()}
        dist = defaultdict(lambda: INF)
        best = INF
        while q:
            cost, node = q.pop()
            if cost >= best:
                continue
            keys, pos = node
            if len(keys) == target:
                if cost < best:
                    best = cost
                    continue

            neighbours = self.get_neighbours(pos, keys)
            for n, d in neighbours.items():
                newkeys = set(keys)
                if n in keynodes:
                    newkeys.add(keynodes[n])

                newnode = (frozenset(newkeys), n)
                newcost = cost + d
                if newcost < dist[newnode]:
                    dist[newnode] = newcost
                    q.set_priority(newnode, newcost)
        return best


class MultiGrid(Grid):
    def __init__(self, grid: Grid):
        self.spaces = grid.spaces
        self.keys = grid.keys
        self.doors = grid.doors
        self.graph = Graph()

        # Modify the grid by splitting the starting space four ways.
        self.starts = {
                (grid.start[0] - 1, grid.start[1] - 1),
                (grid.start[0] - 1, grid.start[1] + 1),
                (grid.start[0] + 1, grid.start[1] - 1),
                (grid.start[0] + 1, grid.start[1] + 1)}
        self.spaces.remove(grid.start)
        self.spaces -= self.get_adjacent(grid.start)
        self.make_graph()

    def make_graph(self):
        """Assemble a graph of the grid space.

        Each square that is an intersection, door, or key will become a node in
        the graph, and linear paths between nodes will become edges.

        In a MultiGrid, this will produce a disconnected graph with four
        subgraphs.
        """
        graph = Graph()
        graph.nodes = set(self.starts)
        explored = set()
        q = [(pos, 0, pos) for pos in self.starts]
        doors = set(self.doors.values())
        keys = set(self.keys.values())
        essentials = self.starts | doors | keys

        while q:
            pos, cost, start = q.pop(0)
            adjacent = self.get_adjacent(pos) & self.spaces - explored
            if len(adjacent) > 1 or pos in essentials:
                graph.nodes.add(pos)
                if cost > 0:
                    graph.edges[start][pos] = cost
                    graph.edges[pos][start] = cost
                cost = 0
                start = pos
            for adj in adjacent:
                q.append((adj, cost + 1, start))
            explored.add(pos)
        self.graph = graph

        # Simplify by removing nodes that only connect between two other nodes.
        # This happens when a position initially looks like an intersection,
        # but further exploration proves some of the branches to be dead ends.
        removable = [
                (k, v) for k, v in graph.edges.items()
                if len(v) == 2 and k not in essentials]
        while removable:
            for node, edges in removable:
                graph.nodes.discard(node)
                graph.edges.pop(node, None)
                others = tuple(edges.keys())
                cost = sum(edges.values())
                for other in others:
                    graph.edges[other].pop(node, None)
                a, b = others
                graph.edges[a][b] = cost
                graph.edges[b][a] = cost
            removable = [
                    (k, v) for k, v in graph.edges.items()
                    if len(v) == 2 and k not in essentials]

    def find_path(self, start: tuple, goal: tuple, keys: set) -> int | None:
        q = PriorityQueue()
        q.push(start, 0)
        keynodes = {v for k, v in self.keys.items() if k not in keys}
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            if node in keynodes:
                return None

            neighbours = self.get_neighbours(node, keys)
            for n, d in neighbours.items():
                score = cost + d
                if score < dist[n]:
                    dist[n] = score
                    priority = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, priority)
        return None

    def find_all_keys_path(self) -> int:
        """Return the fewest steps in which we can gather all keys.

        This is very similar to the routine for a single connected graph,
        except that each node will contain the positions of all four agents,
        and when exploring out from each node we will consider all the
        neighbours of all the agents.
        """
        q = PriorityQueue()
        start = (frozenset(), frozenset(self.starts))
        q.push(start, 0)
        target = len(self.keys)
        keynodes = {v: k for k, v in self.keys.items()}
        dist = defaultdict(lambda: INF)
        dist[start] = 0
        best = INF
        while q:
            priority, node = q.pop()
            cost = dist[node]
            if cost >= best:
                continue
            keys, positions = node
            logging.debug(f"at {positions} with {keys} having moved {cost}")
            if len(keys) == target:
                if cost < best:
                    best = cost
                    continue

            for pos in positions:
                neighbours = self.get_neighbours(pos, keys)
                logging.debug(f"  from {pos} can go to {neighbours}")
                for n, d in neighbours.items():
                    newkeys = set(keys)
                    if n in keynodes:
                        newkeys.add(keynodes[n])

                    newpos = set(positions)
                    newpos.discard(pos)
                    newpos.add(n)
                    newnode = (frozenset(newkeys), frozenset(newpos))
                    newcost = cost + d
                    if newcost < dist[newnode]:
                        dist[newnode] = newcost
                        priority = newcost + (target - len(newkeys)) * 20
                        q.set_priority(newnode, priority)
        return best


def parse(stream) -> Grid:
    return Grid(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.find_all_keys_path()

    with timing("Part 2"):
        if test:
            grid = Grid("""
                    #############
                    #DcBa.#.GhKl#
                    #.###...#I###
                    #e#d#.@.#j#k#
                    ###C#...###J#
                    #fEbA.#.FgHi#
                    #############
                    """)
        multigrid = MultiGrid(grid)
        result2 = multigrid.find_all_keys_path()

    return (result1, result2)
