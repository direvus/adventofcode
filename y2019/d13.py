"""Advent of Code 2019

Day 13: Care Package

https://adventofcode.com/2019/day/13
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing
from y2019.intcode import Computer


class Game:
    def __init__(self):
        self.tiles = defaultdict(lambda: 0)
        self.computer = Computer()
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.score = 0

    def run(self):
        while not self.computer.halt:
            try:
                x = next(self.computer.generate())
                y = next(self.computer.generate())
                v = next(self.computer.generate())
                if (x, y) == (-1, 0):
                    self.score = v
                else:
                    if self.tiles[(x, y)] == 2 and v == 0:
                        blocks = self.count_tiles(2)
                        logging.debug(
                                f"block destroyed at ({x},{y}), "
                                f"{blocks} remain")
                        if blocks == 0:
                            return
                    elif v == 4:
                        self.ball = (x, y)
                    elif v == 3:
                        self.paddle = (x, y)
                    self.tiles[(x, y)] = v
            except StopIteration:
                pass

    def count_tiles(self, value: int) -> int:
        return len(tuple(v for v in self.tiles.values() if v == value))

    def get_control_input(self) -> int:
        """Return an input from the joystick control.

        This is determined from the relative position of the paddle and the
        ball in the game. If the ball is to the left of the paddle, we send it
        left (-1). If the ball is to the right of the paddle, we send it right
        (1). If the ball is directly above the paddle, we leave it neutral (0).
        """
        diff = self.ball[0] - self.paddle[0]
        if diff != 0:
            diff = 1 if diff > 0 else -1
        return diff

    def play(self) -> bool:
        """Play the game.

        Return True if the game is won, or False otherwise. The game is
        considered to be won if at any point there are no blocks remaining. The
        game is considered lost if the game halts with blocks still on the
        grid.
        """
        self.tiles.clear()
        self.ball = (0, 0)
        self.paddle = (0, 0)
        self.score = 0
        self.computer.reset()
        self.computer.memory[0] = 2
        self.computer.set_input_hook(self.get_control_input)
        self.run()
        blocks = self.count_tiles(2)
        logging.debug(f"Game ends with {blocks} blocks, score {self.score}")
        logging.debug(f"Last ball position was {self.ball}")
        return blocks == 0


def parse(stream) -> Game:
    game = Game()
    game.computer.parse(stream.readline().strip())
    return game


def run(stream, test: bool = False):
    if test:
        # No real way to test this, the puzzle did not provide an example
        # input.
        return (0, 0)

    with timing("Part 1"):
        game = parse(stream)
        game.run()
        result1 = game.count_tiles(2)

    with timing("Part 2"):
        game.play()
        result2 = 0

    return (result1, result2)
