"""Advent of Code 2021

Day 4: Giant Squid

https://adventofcode.com/2021/day/4
"""
import logging  # noqa: F401

from util import timing


class Board:
    def __init__(self, stream=''):
        self.numbers = []
        self.marked = set()
        self.win = None
        if stream:
            self.parse(stream)

    def parse(self, stream):
        self.numbers = []
        for line in stream:
            line = line.strip()
            if line == '':
                break
            self.numbers.append(tuple(int(x) for x in line.split()))

    def get_unmarked(self):
        result = set()
        for numbers in self.numbers:
            result |= set(numbers)
        result -= self.marked
        return result

    def mark(self, number: int) -> bool:
        self.marked.add(number)

        for row in self.numbers:
            if all(n in self.marked for n in row):
                self.win = number
                return True

        for col in range(len(self.numbers[0])):
            if all(r[col] in self.marked for r in self.numbers):
                self.win = number
                return True

        return False


class Game:
    def __init__(self, stream):
        self.boards = []
        self.draw = []
        self.counter = 0
        self.winners = set()
        self.parse(stream)

    def parse(self, stream):
        line = stream.readline().strip()
        self.draw = [int(x) for x in line.split(',')]
        # Consume the next blank line
        stream.readline()
        while True:
            board = Board(stream)
            if board.numbers:
                self.boards.append(board)
            else:
                break

    def do_round(self):
        number = self.draw[self.counter]
        self.counter += 1
        result = None

        for i, board in enumerate(self.boards):
            if i in self.winners:
                continue
            win = board.mark(number)
            if win:
                logging.debug(f'{number}: board #{i + 1} wins')
                self.winners.add(i)
                result = number * sum(board.get_unmarked())
        return result

    def play_until_win(self):
        score = None
        while score is None:
            score = self.do_round()
        return score

    def play_until_last_win(self):
        count = len(self.boards)
        while len(self.winners) < count:
            score = self.do_round()
        return score


def parse(stream) -> Game:
    return Game(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = parse(stream)
        result1 = game.play_until_win()

    with timing("Part 2"):
        result2 = game.play_until_last_win()

    return (result1, result2)
