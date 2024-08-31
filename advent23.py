#!/usr/bin/env python
import sys
from collections import namedtuple

from rich import print

from util import timing, Point


Segment = namedtuple('segment', ['start', 'end', 'length', 'choices'])


class Grid:
    def __init__(self):
        self.rows = []
        self.start = None
        self.end = None
        self.head = None

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            if not self.rows:
                self.start = Point(0, line.index('.'))
                self.width = len(line)
            self.rows.append(line)
        self.height = len(self.rows)
        self.end = Point(self.height - 1, line.index('.'))
        self.head = self.find_paths(self.start, set())

    def get_tile(self, point) -> str:
        if (point.y < 0 or point.y >= self.height or
                point.x < 0 or point.x >= self.width):
            return None
        return self.rows[point.y][point.x]

    def is_tile_valid(self, point) -> bool:
        tile = self.get_tile(point)
        return tile is not None and tile != '#'

    def get_neighbours(self, point, visited) -> set:
        """Return all neighbours of the tile that are valid next steps.

        A valid next step must be a path tile that we have not previously
        visited. If the current tile is a slope, the only possible valid
        neighbour is the tile it points to.
        """
        tile = self.get_tile(point)
        match tile:
            case '>':
                n = {Point(point.y, point.x + 1)}
            case '<':
                n = {Point(point.y, point.x - 1)}
            case '^':
                n = {Point(point.y - 1, point.x)}
            case 'v':
                n = {Point(point.y + 1, point.x)}
            case _:
                n = {
                    Point(point.y, point.x + 1),
                    Point(point.y, point.x - 1),
                    Point(point.y - 1, point.x),
                    Point(point.y + 1, point.x),
                    }
        # exclude walls and out-of-bounds
        n = {x for x in n if self.is_tile_valid(x)}
        # exclude already visited
        n -= visited
        return n

    def find_paths(self, start, visited) -> Segment | None:
        """Build a tree of valid paths through the maze."""
        # Take a copy of the visited set and add the start node
        visited = {start} | visited
        # Special case: the starting tile of the map doesn't count as a step
        length = 1 if start != self.start else 0
        end = start
        while True:
            neighbours = self.get_neighbours(end, visited)
            if not neighbours:
                # No valid way forward -> this is a dead end.
                return None
            if len(neighbours) == 1:
                # Only one way forward -> continue this segment.
                length += 1
                (end,) = neighbours
                visited.add(end)
                if end == self.end:
                    # We have reached the goal.
                    return Segment(start, end, length, [])
                continue
            # Multiple ways forward -> recurse into each choice.
            choices = []
            for n in neighbours:
                choice = self.find_paths(n, visited)
                if choice is not None:
                    choices.append(choice)
            return Segment(start, end, length, choices)

    def get_longest_path(self, segment) -> int:
        length = segment.length
        if segment.end == self.end:
            return length
        choice_lengths = [self.get_longest_path(x) for x in segment.choices]
        return length + max(choice_lengths)


if __name__ == '__main__':
    with timing("Part 1\n"):
        grid = Grid()
        grid.parse(sys.stdin)
        result = grid.get_longest_path(grid.head)
    print(f"Result for Part 1 = {result} \n")

    with timing("Part 2\n"):
        result = None
    print(f"Result for Part 2 = {result} \n")
