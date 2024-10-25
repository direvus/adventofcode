"""Advent of Code 2020

Day 22: Crab Combat

https://adventofcode.com/2020/day/22
"""
import logging  # noqa: F401
from collections import deque

from util import timing


class Game:
    def __init__(self, stream):
        self.players = []
        self.decks = []
        self.counter = 0

        if stream:
            self.parse(stream)

    def parse(self, stream):
        line = stream.readline().strip()
        while line:
            name = line[:-1]
            self.players.append(name)
            deck = deque()
            for line in stream:
                line = line.strip()
                if line == '':
                    break
                card = int(line)
                deck.append(card)
            self.decks.append(deck)
            line = stream.readline().strip()

    def do_round(self):
        draws = []
        for i in range(len(self.players)):
            draw = self.decks[i].popleft()
            draws.append((draw, i))
        draws.sort(reverse=True)
        winner = draws[0][1]
        for card, _ in draws:
            self.decks[winner].append(card)

    def play(self) -> int:
        """Play until one player has all the cards.

        Return the index of the winner player.
        """
        while all(deck for deck in self.decks):
            self.do_round()
            self.counter += 1
        decksize = [(len(d), i) for i, d in enumerate(self.decks)]
        decksize.sort(reverse=True)
        return decksize[0][1]

    def get_score(self, player: int) -> int:
        result = 0
        cards = reversed(list(self.decks[player]))
        for i, card in enumerate(cards):
            result += (i + 1) * card
        return result


def parse(stream) -> Game:
    return Game(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = parse(stream)
        winner = game.play()
        result1 = game.get_score(winner)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
