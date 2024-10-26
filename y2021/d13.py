"""Advent of Code 2021

Day 13: Transparent Origami

https://adventofcode.com/2021/day/13
"""
import logging  # noqa: F401

from util import timing


class Grid:
    def __init__(self, dots):
        self.dots = set(dots)

    def do_fold(self, fold):
        axis, value = fold
        dots = set()
        for p in self.dots:
            x, y = p
            if axis == 'y':
                if y > value:
                    y = value - (y - value)
            else:
                if x > value:
                    x = value - (x - value)
            dots.add((x, y))
        self.dots = dots

    def __str__(self):
        lines = []
        maxy = max(p[1] for p in self.dots)
        maxx = max(p[0] for p in self.dots)
        for y in range(maxy + 1):
            line = []
            for x in range(maxx + 1):
                p = (x, y)
                ch = '#' if p in self.dots else '.'
                line.append(ch)
            lines.append(''.join(line))
        return '\n'.join(lines)


def parse(stream) -> str:
    dots = set()
    for line in stream:
        line = line.strip()
        if line == '':
            break
        pos = tuple(int(x) for x in line.split(','))
        dots.add(pos)

    folds = []
    for line in stream:
        line = line.strip()
        words = line.split()
        axis, value = words[-1].split('=')
        value = int(value)
        folds.append((axis, value))
    return dots, folds


def run(stream, test: bool = False):
    with timing("Part 1"):
        dots, folds = parse(stream)
        logging.debug(dots)
        logging.debug(folds)
        grid = Grid(dots)
        grid.do_fold(folds[0])
        result1 = len(grid.dots)

    with timing("Part 2"):
        for fold in folds[1:]:
            grid.do_fold(fold)
        result2 = str(grid)

    return (result1, result2)
