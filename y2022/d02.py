"""Advent of Code 2022

Day 2: Rock Paper Scissors

https://adventofcode.com/2022/day/2
"""
import logging  # noqa: F401

from util import timing

SCORES = (1, 2, 3)
CODES = {'A': 0, 'X': 0, 'B': 1, 'Y': 1, 'C': 2, 'Z': 2}


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        words = line.split()
        choices = (CODES[x] for x in words)
        result.append(tuple(choices))
    return result


def get_total_score(rounds) -> int:
    result = 0
    for opp, player in rounds:
        result += SCORES[player]
        if opp == player:
            # Draw
            result += 3
        elif player == (opp + 1) % 3:
            # Win
            result += 6
    return result


def get_total_score_part2(rounds) -> int:
    result = 0
    for opp, strategy in rounds:
        if strategy == 0:
            # Must lose
            choice = (opp - 1) % 3
        elif strategy == 1:
            # Must draw
            choice = opp
            result += 3
        else:
            # Must win
            choice = (opp + 1) % 3
            result += 6
        result += SCORES[choice]
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = get_total_score(parsed)

    with timing("Part 2"):
        result2 = get_total_score_part2(parsed)

    return (result1, result2)
