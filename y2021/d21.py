"""Advent of Code 2021

Day 21: Dirac Dice

https://adventofcode.com/2021/day/21
"""
import logging  # noqa: F401
from collections import deque

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


def calculate_wins(pos1, pos2, win_score: int = 21) -> tuple:
    """Calculate the win count under the Part 2 rules.

    Assuming each turn rolls 3d3, and with the players' starting positions and
    required score to win, determine how many ways each player can win the
    game.

    Return the win counts for both players as a tuple.
    """
    # Frequencies of total rolls on 3d3
    freqs = ((3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1))
    q = deque()
    q.append((1, 0, (pos1 - 1, pos2 - 1), (0, 0)))
    wins = [0, 0]
    while q:
        ways, turns, positions, scores = q.pop()
        player = turns % 2
        turns += 1
        pos = positions[player]
        for roll, freq in freqs:
            p = (pos + roll) % 10
            s = scores[player] + p + 1
            if s >= win_score:
                wins[player] += ways * freq
            else:
                newpos = list(positions)
                newscores = list(scores)
                newpos[player] = p
                newscores[player] = s
                q.append((ways * freq, turns, newpos, newscores))
    return tuple(wins)


def run(stream, test: bool = False):
    with timing("Part 1"):
        pos1, pos2 = parse(stream)
        game = Game(Die(100), pos1, pos2)
        game.do_turn()
        game.play()
        result1 = min(game.scores) * game.turns * 3

    with timing("Part 2"):
        win_score = 5 if test else 21
        wins = calculate_wins(pos1, pos2, win_score)
        logging.debug(wins)
        result2 = max(wins)

    return (result1, result2)
