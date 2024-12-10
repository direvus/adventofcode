"""Advent of Code 2024

Day 10: _TITLE_

https://adventofcode.com/2024/day/10
"""
import logging  # noqa: F401
from collections import defaultdict, deque

import grid
from util import timing, INF, PriorityQueue


class Grid(grid.Grid):
    starts = set()
    goals = set()

    def parse_cell(self, position, value):
        value = int(value)
        if value == 0:
            self.starts.add(position)
        elif value == 9:
            self.goals.add(position)
        return value

    def get_value(self, position):
        return self.cells[position[1]][position[0]]

    def get_neighbours(self, position):
        target = self.get_value(position) + 1
        return {
                x for x in self.get_adjacent(position)
                if self.get_value(x) == target}

    def has_path(self, start, goal) -> bool:
        # AStar
        q = PriorityQueue()
        q.push(start, grid.get_distance(start, goal))
        dist = defaultdict(lambda: INF)
        dist[start] = 0

        while q:
            est, node = q.pop()
            if node == goal:
                return True

            for n in self.get_neighbours(node):
                score = dist[node] + 1
                if score < dist[n]:
                    dist[n] = score
                    f = score + grid.get_distance(n, goal)
                    q.set_priority(n, f)
        return False

    def count_paths(self, start) -> int:
        """Return the number of distinct paths from start to any goal."""
        result = 0
        # BFS
        q = deque()
        q.append(start)

        while q:
            node = q.pop()
            if node in self.goals:
                result += 1
                continue

            for n in self.get_neighbours(node):
                q.append(n)
        return result

    def get_trailhead_score(self, start):
        result = 0
        for goal in self.goals:
            if self.has_path(start, goal):
                result += 1
        return result

    def get_trailhead_scores(self):
        result = []
        for start in self.starts:
            score = self.get_trailhead_score(start)
            result.append(score)
        return result

    def get_trailhead_rating(self, start):
        return self.count_paths(start)

    def get_total_rating(self):
        return sum(self.get_trailhead_rating(x) for x in self.starts)


def parse(stream) -> str:
    return stream.readline().strip()


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid().parse(stream)
        result1 = sum(grid.get_trailhead_scores())

    with timing("Part 2"):
        result2 = grid.get_total_rating()

    return (result1, result2)
