"""Advent of Code 2024

Day 6: Guard Gallivant

https://adventofcode.com/2024/day/6
"""
import logging  # noqa: F401

from util import timing


FACING = ((0, -1), (1, 0), (0, 1), (-1, 0))


def parse(stream) -> str:
    blocked = set()
    start = None
    width = 0
    height = 0
    y = 0
    for line in stream:
        for x, ch in enumerate(line):
            if ch == '#':
                blocked.add((x, y))
            elif ch == '^':
                start = (x, y)
        y += 1
    height = y
    width = x + 1
    return height, width, start, blocked


def get_positions(height, width, start, blocked):
    x, y = start
    result = set()
    facing = 0
    while x >= 0 and x < width and y >= 0 and y < height:
        result.add((x, y))
        vx, vy = FACING[facing]
        newpos = x + vx, y + vy
        if newpos in blocked:
            facing = (facing + 1) % 4
        else:
            x, y = newpos
    return result


def print_grid(height, width, blocked, visited):
    lines = []
    for y in range(height):
        line = []
        for x in range(width):
            p = (x, y)
            ch = '#' if p in blocked else 'X' if p in visited else '.'
            line.append(ch)
        lines.append(''.join(line))
    print('\n'.join(lines))


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        visited = get_positions(*parsed)
        print_grid(parsed[0], parsed[1], parsed[3], visited)
        result1 = len(visited)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
