"""Advent of Code 2020

Day 22: Crab Combat

https://adventofcode.com/2020/day/22
"""
import logging  # noqa: F401
from collections import deque
from functools import cache

from util import timing


class Game:
    def __init__(self, stream=''):
        self.decks = []
        self.counter = 0

        if stream:
            self.parse(stream)

    def parse(self, stream):
        line = stream.readline().strip()
        while line:
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
        for i in range(len(self.decks)):
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

    def get_decks(self) -> tuple:
        return tuple(tuple(d) for d in self.decks)


class RecursiveGame(Game):
    def __init__(self, stream=''):
        super().__init__(stream)
        self.history = []
        self.winner = None
        self.total = sum(len(d) for d in self.decks)

    def do_round(self):
        # Check for a loop
        config = self.get_decks()
        if config in self.history:
            self.winner = 0
            return

        # Record a copy of the current state for loop prevention.
        self.history.append(self.get_decks())

        draws = []
        for i in range(len(self.decks)):
            draw = self.decks[i].popleft()
            draws.append((draw, i))

        # Do we recurse into a sub-game here?
        if all(n <= len(self.decks[i]) for n, i in draws):
            # Winner of the round is determined by the winner of the sub-game.
            decks = []
            # Take a copy of the top N cards from each player's deck, where N
            # is the value of the card they drew.
            for card, player in draws:
                deck = tuple(self.decks[player])[:card]
                decks.append(deck)
            winner = play_game(tuple(decks))

            # Winner's card goes to the top, even if it's not the high card.
            draws.sort(key=lambda x: x[1] != winner)
        else:
            # Winner is determined by high card, as in Part 1.
            draws.sort(reverse=True)
            winner = draws[0][1]

        for card, _ in draws:
            self.decks[winner].append(card)

        # If the winner of the round now has all the cards, they have won the
        # overall game.
        if len(self.decks[winner]) == self.total:
            self.winner = winner

    def play(self) -> int:
        """Play until the game ends.

        Return the index of the winning player.
        """
        self.winner is None
        self.total = sum(len(d) for d in self.decks)
        self.history = []
        while self.winner is None:
            self.do_round()
            self.counter += 1
        return self.winner


@cache
def play_game(decks: tuple) -> int:
    game = RecursiveGame()
    game.decks = [deque(d) for d in decks]
    return game.play()


def parse(stream) -> Game:
    return Game(stream)


def run(stream, test: bool = False):
    with timing("Part 1"):
        game = parse(stream)

        # Take a copy of the initial state so we can re-use it in Part 2.
        decks = game.get_decks()

        winner = game.play()
        result1 = game.get_score(winner)

    with timing("Part 2"):
        game = RecursiveGame()
        game.decks = [deque(d) for d in decks]
        winner = game.play()
        result2 = game.get_score(winner)

    return (result1, result2)
