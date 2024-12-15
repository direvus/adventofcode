"""Advent of Code 2024

Day 15: Warehouse Woes

https://adventofcode.com/2024/day/15
"""
import logging  # noqa: F401

from util import timing
import grid


class Grid(grid.SparseGrid):
    def __init__(self):
        super().__init__()
        self.walls = set()
        self.boxes = set()
        self.start = None

    def parse_cell(self, position: tuple, value: str | int):
        if value == '#':
            self.walls.add(position)
        elif value == 'O':
            self.boxes.add(position)
        elif value == '@':
            self.start = position

    def do_move(self, position, direction: int):
        boxes = set()
        ahead = position
        while True:
            ahead = grid.move(ahead, direction)
            if ahead in self.boxes:
                boxes.add(ahead)
            elif ahead in self.walls:
                # Move not possible
                return position
            else:
                break
        # Remove all the boxes that are getting pushed, then re-add them in
        # their new positions.
        self.boxes -= boxes
        for box in boxes:
            self.boxes.add(grid.move(box, direction))
        return grid.move(position, direction)

    def do_moves(self, moves):
        position = self.start
        for move in moves:
            position = self.do_move(position, move)

    def get_total_box_score(self):
        return sum(map(get_box_score, self.boxes))

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                p = (x, y)
                ch = (
                        '#' if p in self.walls else
                        'O' if p in self.boxes else
                        '.')
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> str:
    data = stream.read()
    plan, moves = data.split('\n\n')
    plan = plan.split('\n')
    moves = ''.join(moves.split())
    moves = map(lambda x: grid.FACING.index(x), moves.strip())
    return plan, moves


def get_box_score(position) -> int:
    return position[0] + (position[1] * 100)


def run(stream, test: bool = False):
    with timing("Part 1"):
        plan, moves = parse(stream)
        grid = Grid().parse(plan)
        grid.do_moves(moves)
        result1 = grid.get_total_box_score()

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
