"""Advent of Code 2021

Day 21: Dirac Dice

https://adventofcode.com/2021/day/21
"""
import logging  # noqa: F401

from util import timing


class Die:
    def __init__(self, sides: int):
        self.sides = sides
        self.counter = 0

    def roll(self) -> int:
        if self.counter > 99:
            self.counter = 1
        else:
            self.counter += 1
        return self.counter


class Game:
    def __init__(self, die, pos1, pos2):
        self.die = die
        self.players = [pos1 - 1, pos2 - 1]
        self.scores = [0, 0]
        self.turns = 0

    def do_turn(self):
        player = self.turns % 2
        pos = self.players[player]
        roll = sum(self.die.roll() for _ in range(3))
        pos = (pos + roll) % 10
        self.players[player] = pos
        self.scores[player] += pos + 1
        self.turns += 1

    def play(self):
        while all(x < 1000 for x in self.scores):
            self.do_turn()


def parse(stream) -> str:
    result = []
    for line in stream:
        prefix, pos = line.strip().split(': ')
        result.append(int(pos))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        pos1, pos2 = parse(stream)
        game = Game(Die(100), pos1, pos2)
        game.do_turn()
        logging.debug(vars(game))
        game.play()
        logging.debug(game.scores)
        logging.debug(game.turns)
        result1 = min(game.scores) * game.turns * 3

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
