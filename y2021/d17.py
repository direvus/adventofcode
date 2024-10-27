"""Advent of Code 2021

Day 17: Trick Shot

https://adventofcode.com/2021/day/17
"""
import logging  # noqa: F401

from util import timing, NINF


def parse(stream) -> tuple:
    line = stream.readline().strip()
    coords = line[13:]
    x, y = coords.split(', ')
    x1, x2 = (int(v) for v in x[2:].split('..'))
    y1, y2 = (int(v) for v in y[2:].split('..'))
    return (x1, x2, y1, y2)


def shoot(velocity: tuple, target: tuple) -> int | None:
    """Fire a probe with the given velocity and target area.

    Return the probe's maximum Y-value reached, if it hit the target area, or
    None if it missed.
    """
    x = 0
    y = 0
    maxy = NINF
    vx, vy = velocity
    # This code relies on the target area being entirely to the right of, and
    # entirely below, the origin.
    assert target[0] > 0
    assert target[0] < target[1]
    assert target[3] < 0
    assert target[2] < target[3]

    while x <= target[1] and y >= target[2]:
        x += vx
        y += vy
        if y > maxy:
            maxy = y

        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        elif x < target[0]:
            # If X has stabilised and we're not over the target area, then
            # we've fallen short
            return None

        vy -= 1
        logging.debug((x, y))
        if (
                x >= target[0] and x <= target[1] and
                y >= target[2] and y <= target[3]):
            # A hit, very possibly a palpable one.
            return maxy
    return None


def find_min_vx(target: tuple) -> int:
    """Find the minimum X velocity that can possibly hit the target.

    X velocities less than this value will always fall short of the target box.
    """
    result = target[0]
    while result > 0:
        vx = result
        x = 0
        while vx != 0:
            x += vx
            vx -= 1
        if x < target[0]:
            return result + 1
        result -= 1


def find_highest(target: tuple) -> tuple:
    min_vx = find_min_vx(target)
    max_vx = target[1]
    min_vy = target[2]
    max_vy = -target[2]
    best = NINF
    hits = 0

    for vx in range(min_vx, max_vx + 1):
        for vy in range(min_vy, max_vy + 1):
            height = shoot((vx, vy), target)
            if height is None:
                continue
            hits += 1
            if height > best:
                best = height
    return hits, best


def run(stream, test: bool = False):
    with timing("Both parts"):
        target = parse(stream)
        result2, result1 = find_highest(target)

    return (result1, result2)
