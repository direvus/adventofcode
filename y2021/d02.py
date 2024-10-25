"""Advent of Code 2021

Day 2: Dive!

https://adventofcode.com/2021/day/2
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        direction, distance = line.split()
        result.append((direction, int(distance)))
    return result


def move(position: tuple, direction: str, distance: int) -> tuple:
    x, y = position
    match direction:
        case 'forward':
            return (x + distance, y)
        case 'down':
            return (x, y + distance)
        case 'up':
            return (x, y - distance)


def move2(position: tuple, direction: str, distance: int) -> tuple:
    x, y, a = position
    match direction:
        case 'forward':
            return (x + distance, y + a * distance, a)
        case 'down':
            return (x, y, a + distance)
        case 'up':
            return (x, y, a - distance)


def do_moves(moves: list) -> tuple:
    p = (0, 0)
    for direction, distance in moves:
        p = move(p, direction, distance)
    return p


def do_moves2(moves: list) -> tuple:
    p = (0, 0, 0)
    for direction, distance in moves:
        p = move2(p, direction, distance)
    return p


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        position = do_moves(parsed)
        result1 = position[0] * position[1]

    with timing("Part 2"):
        x, y, a = do_moves2(parsed)
        result2 = x * y

    return (result1, result2)
