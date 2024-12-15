"""Advent of Code 2024

Day 14: Restroom Redoubt

https://adventofcode.com/2024/day/14
"""
import bisect
import logging  # noqa: F401
from collections import OrderedDict
from math import prod
from operator import add, mod

import visualise
from util import timing


def ease_cubic_in_out(x):
    if x < 0.5:
        return 4 * (x ** 3)
    else:
        return 1 - ((x * -2 + 2) ** 3) / 2


def position_to_image_coords(position):
    return tuple(map(lambda v: 1 + 5 * v, position))


class Sprite(visualise.Sprite):
    def __init__(self, grid_size, *args, **kwargs):
        self.grid_size = grid_size
        self.transitions = OrderedDict()
        kwargs['final_status'] = visualise.Status.PERMANENT
        super().__init__(*args, **kwargs)

    def add_transition(self, start, duration, source, vector):
        self.transitions[start] = (start, duration, source, vector)
        self.stop = start + duration

    def get_position(self, canvas, time):
        keys = list(self.transitions.keys())
        key = bisect.bisect_right(keys, time)
        if not key:
            return position_to_image_coords(self.position)
        index = keys[key - 1]
        start, duration, source, vector = self.transitions[index]
        end = start + duration
        if end <= time:
            # It's already completed
            dest = tuple(map(mod, map(add, source, vector), self.grid_size))
            coords = position_to_image_coords(dest)
            return coords
        progress = (time - start) / duration
        easing = ease_cubic_in_out(progress)
        vector = map(lambda v: v * easing, vector)
        position = map(mod, map(add, source, vector), self.grid_size)
        coords = position_to_image_coords(position)
        result = tuple(map(round, coords))
        return result


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


def generate_christmas_tree(width, height) -> set:
    result = set()
    minx = width // 2
    maxx = width // 2 + 1
    for y in range(min(width, height) - 1):
        for x in range(minx, maxx):
            result.add((x, y))
        minx -= 1
        maxx += 1
    return result


def get_text(width, height, positions):
    lines = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append('#' if (x, y) in positions else '.')
        lines.append(''.join(line))
    return '\n'.join(lines)


def find_christmas_tree(width, height, robots, draw: bool = False):
    if draw:
        pixels = (
                'assets/green_pixel_4.png',
                'assets/green_pixel_4.png',
                'assets/green_pixel_4.png',
                'assets/green_pixel_4.png',
                'assets/gold_pixel_4.png',
                'assets/red_pixel_4.png',
                )
        # Allow 4 pixels per tile, plus border.
        grid_size = (width, height)
        size = (5 * width + 1, 5 * height + 1)
        im = visualise.Animation(size, 24, '#1a1a1a')
        sprites = []
        for i in range(len(robots)):
            pixel = pixels[i % len(pixels)]
            sprite = Sprite(
                    grid_size, pixel, robots[i][:2], start=0, fade_in=6)
            sprites.append(sprite)
            im.add_element(sprite)

    pattern = generate_christmas_tree(width, height)
    threshold = len(robots) * 0.9
    i = 0
    t = 6
    rate = 32
    trans = round(rate * 0.8)

    while True:
        positions = {(x, y) for x, y, _, _ in robots}
        if len(positions & pattern) > threshold:
            if draw:
                im.render('out/y2024d14.gif', t - rate * 5, t)
            return i
        new = []
        for r in range(len(robots)):
            x, y, vx, vy = robots[r]
            nx, ny = move(width, height, x, y, vx, vy)
            new.append((nx, ny, vx, vy))
            if draw:
                sprites[r].add_transition(t + 2, trans, (x, y), (vx, vy))
        robots = new
        i += 1
        t += rate


def run(stream, test: bool = False, draw: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        width = 11 if test else 101
        height = 7 if test else 103
        robots = do_moves(width, height, parsed, 100)
        result1 = get_score(width, height, robots)

    with timing("Part 2"):
        if not test:
            result2 = find_christmas_tree(width, height, parsed, draw)
        else:
            # No way to run Part 2 on the example input.
            result2 = 0

    return (result1, result2)
