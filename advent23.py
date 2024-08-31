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
        self.segments = {}
        self.slopes = True

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            if not self.rows:
                self.start = Point(0, line.index('.'))
                self.width = len(line)
            self.rows.append(line)
        self.height = len(self.rows)
        self.end = Point(self.height - 1, line.index('.'))
        self.segments = {}
        self.head = self.find_paths(self.start, set())

    def get_tile(self, point) -> str:
        if (point.y < 0 or point.y >= self.height or
                point.x < 0 or point.x >= self.width):
            return None
        return self.rows[point.y][point.x]

    def is_tile_valid(self, point) -> bool:
        tile = self.get_tile(point)
        return tile is not None and tile != '#'

    def get_neighbours(self, point) -> set:
        """Return all neighbours of the tile that are valid next steps.

        If the current tile is a slope, and the grid is in slopes mode, the
        only possible valid neighbour is the tile it points to.
        """
        tile = self.get_tile(point)
        if self.slopes and tile in '><^v':
            match tile:
                case '>':
                    n = {Point(point.y, point.x + 1)}
                case '<':
                    n = {Point(point.y, point.x - 1)}
                case '^':
                    n = {Point(point.y - 1, point.x)}
                case 'v':
                    n = {Point(point.y + 1, point.x)}
        elif point == self.start:
            n = {Point(point.y + 1, point.x)}
        else:
            n = {
                Point(point.y, point.x + 1),
                Point(point.y, point.x - 1),
                Point(point.y - 1, point.x),
                Point(point.y + 1, point.x),
                }
        # exclude walls and out-of-bounds
        n = {x for x in n if self.is_tile_valid(x)}
        return n

    def reset_paths(self):
        self.segments = {}
        self.head = None

    def find_paths(self, start, prev=None) -> Point | None:
        """Build a tree of valid paths through the maze."""
        if start in self.segments:
            # We've already explored this start point, don't repeat
            return start
        # Special case: the starting tile of the map doesn't count as a step
        length = 1 if start != self.start else 0
        end = start
        while True:
            neighbours = self.get_neighbours(end)
            if prev:
                neighbours.discard(prev)
            if not neighbours:
                # No valid way forward -> this is a dead end.
                return None
            if len(neighbours) == 1:
                # Only one way forward -> continue this segment.
                length += 1
                prev = end
                (end,) = neighbours
                if end == self.end:
                    # We have reached the goal.
                    segment = Segment(start, end, length, [])
                    self.segments[start] = segment
                    return start
                continue
            # Multiple ways forward -> recurse into each choice.
            choices = []
            segment = Segment(start, end, length, choices)
            self.segments[start] = segment
            for n in neighbours:
                choice = self.find_paths(n, end)
                if choice is not None:
                    choices.append(choice)
            if not choices:
                return None
            return start

    def get_longest_path(
            self, start, visited) -> tuple[int, list[Point]] | None:
        segment = self.segments[start]
        if start in visited or segment.end in visited:
            return None
        if segment.end == self.end:
            return segment.length, [segment.end]
        visited = visited | {start, segment.end}
        choices = [
                (self.get_longest_path(x, visited), x)
                for x in segment.choices
                if x not in visited]
        choices = list(filter(lambda x: x[0] is not None, choices))
        if not choices:
            return None
        choices.sort(key=lambda x: x[0][0], reverse=True)
        (length, path), choice = choices[0]
        path.insert(0, choice)
        return segment.length + length, path

    def get_longest_path_length(self, start, visited=None) -> int | None:
        if visited is None:
            visited = set()
        segment = self.segments[start]
        if start in visited or segment.end in visited:
            return None
        if segment.end == self.end:
            return segment.length
        visited = visited | {start, segment.end}
        choices = [
                self.get_longest_path_length(x, visited)
                for x in segment.choices
                if x not in visited]
        choices = list(filter(lambda x: x is not None, choices))
        if not choices:
            return None
        return segment.length + max(choices)


if __name__ == '__main__':
    with timing("Part 1\n"):
        grid = Grid()
        grid.parse(sys.stdin)
        result = grid.get_longest_path_length(grid.head)
    print(f"Result for Part 1 = {result} \n")

    with timing("Part 2\n"):
        grid.reset_paths()
        grid.slopes = False
        grid.head = grid.find_paths(grid.start)
        result = grid.get_longest_path_length(grid.head)
    print(f"Result for Part 2 = {result} \n")
