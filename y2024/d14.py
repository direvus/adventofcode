"""Advent of Code 2024

Day 14: Restroom Redoubt

https://adventofcode.com/2024/day/14
"""
import logging  # noqa: F401
from math import prod

from util import timing


def parse(stream) -> str:
    result = []
    for line in stream:
        p, v = line.strip().split(' ')
        px, py = map(int, p[2:].split(','))
        vx, vy = map(int, v[2:].split(','))
        result.append((px, py, vx, vy))
    return result


def move(width, height, px, py, vx, vy):
    x = (px + vx) % width
    y = (py + vy) % height
    return (x, y)


def get_score(width, height, robots):
    quadrants = {
            (0, 0): 0,
            (1, 0): 0,
            (0, 1): 0,
            (1, 1): 0,
            }
    cx = width // 2
    cy = height // 2
    for x, y, vx, vy in robots:
        if x == cx or y == cy:
            # It's not a member of any quadrant
            continue
        qx = int(x > cx)
        qy = int(y > cy)
        quadrants[(qx, qy)] += 1
    return prod(quadrants.values())


def do_moves(width, height, robots, count):
    for i in range(count):
        new = []
        for x, y, vx, vy in robots:
            x, y = move(width, height, x, y, vx, vy)
            new.append((x, y, vx, vy))
        robots = new
    return robots


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        width = 11 if test else 101
        height = 7 if test else 103
        robots = do_moves(width, height, parsed, 100)
        result1 = get_score(width, height, robots)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
