"""Advent of Code 2019

Day 15: Oxygen System

https://adventofcode.com/2019/day/15
"""
import logging  # noqa: F401
from collections import defaultdict

from util import INF, PriorityQueue, get_manhattan_distance, timing
from y2019.intcode import Computer


DIRECTIONS = 'NSWE'
REVERSALS = (1, 0, 3, 2)
VECTORS = ((0, -1), (0, 1), (-1, 0), (1, 0))


def move(point: tuple, direction: int) -> tuple:
    v = VECTORS[direction]
    return (point[0] + v[0], point[1] + v[1])


class Grid:
    def __init__(self, stream=None):
        self.walls = set()
        self.spaces = {(0, 0)}
        self.position = (0, 0)
        self.target = (0, 0)
        self.goal = None
        self.halt = False
        self.robot = Computer()
        self.robot.set_input_hook(self.get_next_input)
        self.moves = []

        if stream:
            self.parse(stream)

    def parse(self, stream):
        self.robot.parse(stream)

    def run(self):
        while not self.halt:
            status = next(self.robot.generate())
            if status == 2:
                # Found the goal
                self.position = self.target
                self.spaces.add(self.position)
                self.goal = self.position
            elif status == 1:
                # Empty space
                self.position = self.target
                self.spaces.add(self.position)
            elif status == 0:
                # Wall
                self.walls.add(self.target)
                self.moves.pop()

    def get_unexplored_neighbour(self) -> tuple | None:
        """Return an unexplored neighbour of the current position.

        The return is a tuple containing an integer index into DIRECTIONS and
        the coordinates of a square that is adjacent to the current position
        and unexplored, or None if no such square exists.
        """
        explored = self.walls | self.spaces
        for i in range(len(DIRECTIONS)):
            p = move(self.position, i)
            if p not in explored:
                return (i, p)
        return None

    def get_neighbours(self, position: tuple) -> set:
        """Return all neighbouring spaces of `position`.

        The return value is a set of coordinate tuples.
        """
        result = set()
        for i in range(len(DIRECTIONS)):
            p = move(position, i)
            if p in self.spaces:
                result.add(p)
        return result

    def get_next_input(self) -> int:
        """Return the next direction input for the robot.

        If there is an unexplored space adjacent to the current space, move
        into it. Otherwise, backtrack along the path. If there is nowhere left
        to backtrack, we have fully explored the space.
        """
        neighbour = self.get_unexplored_neighbour()
        if neighbour:
            direction, target = neighbour
            self.moves.append(direction)
            self.target = target
        else:
            if self.moves:
                last = self.moves.pop()
                direction = REVERSALS[last]
                self.target = move(self.position, direction)
            else:
                # Fully explored, just send any direction so that the robot
                # will complete its iteration and then stop.
                self.halt = True
                direction = 0
                self.target = move(self.position, direction)
        return direction + 1  # Movement commands are 1-based

    def find_path(self, start: tuple, goal: tuple) -> int | None:
        """Find the shortest path from `start` to `goal`.

        Return the number of steps in the shortest path, or None if the goal is
        not reachable.
        """
        q = PriorityQueue()
        q.push(start, get_manhattan_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            cost, node = q.pop()
            if node == goal:
                return cost

            for n in self.get_neighbours(node):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + get_manhattan_distance(n, goal)
                    q.set_priority(n, f)
        return None

    def get_steps_to_goal(self) -> int | None:
        """Return the number of steps between the start and the goal.

        First we need to figure out where the goal is, so fully explore the
        space with the robot, and then find the shortest path to the goal from
        the origin.

        Return the length of that shortest path.
        """
        self.run()
        return self.find_path((0, 0), self.goal)

    def to_string(self) -> str:
        squares = self.walls | self.spaces
        xs = {p[0] for p in squares}
        ys = {p[1] for p in squares}
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)

        lines = []
        for y in range(miny, maxy + 1):
            line = []
            for x in range(minx, maxx + 1):
                p = (x, y)
                if p == self.position:
                    ch = '*'
                elif p == (0, 0):
                    ch = 'O'
                elif p == self.goal:
                    ch = 'X'
                elif p in self.walls:
                    ch = '#'
                elif p in self.spaces:
                    ch = '.'
                else:
                    ch = ' '
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> Grid:
    program = stream.readline().strip()
    grid = Grid(program)
    return grid


def run(stream, test: bool = False):
    if test:
        return (0, 0)

    with timing("Part 1"):
        grid = parse(stream)
        result1 = grid.get_steps_to_goal()
        print(grid.to_string())

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
