"""Advent of Code 2018

Day 13: Mine Cart Madness

https://adventofcode.com/2018/day/13
"""
import logging  # noqa: F401
from collections import Counter
from copy import deepcopy
from io import StringIO

from util import timing


DIRECTIONS = ('^', '>', 'v', '<')
TURNS = (-1, 0, 1)
VECTORS = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
        }
REFLECTIONS = {
        ('/', '^'): '>',
        ('/', '>'): '^',
        ('/', 'v'): '<',
        ('/', '<'): 'v',
        ('\\', '^'): '<',
        ('\\', '>'): 'v',
        ('\\', 'v'): '>',
        ('\\', '<'): '^',
        }


def move(position: tuple, direction: str) -> tuple:
    vy, vx = VECTORS[direction]
    return (position[0] + vy, position[1] + vx)


def turn(direction: str, count: int = 1) -> str:
    """Change direction by `count` increments of 90 degrees clockwise."""
    index = DIRECTIONS.index(direction)
    index = (index + count) % 4
    return DIRECTIONS[index]


class Cart:
    def __init__(self, cartid: int, position: tuple, direction: str):
        self.cartid = cartid
        self.position = position
        self.direction = direction
        self.turn = 0

    def move(self) -> tuple:
        self.position = move(self.position, self.direction)
        return self.position

    def update(self, cell: str):
        if cell in {'/', '\\'}:
            self.direction = REFLECTIONS[(cell, self.direction)]
        elif cell == '+':
            self.direction = turn(self.direction, TURNS[self.turn])
            self.turn = (self.turn + 1) % 3


class Grid:
    def __init__(self):
        self.carts = {}
        self.tracks = {}
        self.collisions = []
        self.time = 0

    def parse(self, stream):
        y = 0
        cartid = 0
        for line in stream:
            for x, ch in enumerate(line):
                if ch in {'/', '\\', '+'}:
                    self.tracks[(x, y)] = ch
                elif ch in DIRECTIONS:
                    self.carts[cartid] = Cart(cartid, (x, y), ch)
                    cartid += 1
            y += 1

    def update(self):
        carts = list(self.carts.values())
        carts.sort(key=lambda x: tuple(reversed(x.position)))
        removed = set()
        for cart in carts:
            if cart.cartid in removed:
                continue
            cart.move()
            collision = self.get_collision()
            if collision is not None:
                self.collisions.append(collision)
                collided = {x.cartid for x in carts if x.position == collision}
                for cartid in collided:
                    removed.add(cartid)
                    del self.carts[cartid]
            else:
                pos = cart.position
                if pos in self.tracks:
                    cart.update(self.tracks[pos])
        self.time += 1

    def get_collision(self) -> tuple | None:
        counter = Counter(c.position for c in self.carts.values())
        pos, count = counter.most_common(1)[0]
        if count > 1:
            return pos

    def find_first_collision(self) -> tuple:
        while not self.collisions:
            self.update()
        return self.collisions[0]

    def find_last_cart(self) -> tuple:
        while len(self.carts) > 1:
            self.update()
        return next(iter(self.carts.values())).position


def run(stream, test: bool = False):
    with timing("Part 1"):
        grid = Grid()
        grid.parse(stream)
        grid2 = deepcopy(grid)
        result1 = grid.find_first_collision()

    with timing("Part 2"):
        # The test cast is different for Part 2
        if test:
            source = '\n'.join([
                    r"/>-<\   ",
                    r"|   |   ",
                    r"| /<+-\ ",
                    r"| | | v ",
                    r"\>+</ | ",
                    r"  |   ^ ",
                    r"  \<->/ "]) + '\n'
            grid2 = Grid()
            grid2.parse(StringIO(source))
        result2 = grid2.find_last_cart()

    return (result1, result2)
