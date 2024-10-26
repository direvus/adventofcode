"""Advent of Code 2021

Day 10: Syntax Scoring

https://adventofcode.com/2021/day/10
"""
import logging  # noqa: F401

from util import timing


OPENERS = '([{<'
CLOSERS = ')]}>'
ERROR_SCORES = (3, 57, 1197, 25137)
COMPLETE_SCORES = (1, 2, 3, 4)


def parse(stream) -> list:
    result = []
    for line in stream:
        line = line.strip()
        result.append(line)
    return result


def get_scores(line: str) -> tuple[int]:
    """Return the scores for this line.

    The first score is the syntax error score. For lines with an invalid
    closing character, it is the score value for that closing character, or
    zero if there are no invalid closures.

    The second score is the autocomplete score. For lines that had an invalid
    closure, this will be zero. Otherwise the score is formed by successively
    multiplying by five and adding the completion score for each missing
    closure.
    """
    stack = []
    error_score = 0
    complete_score = 0
    for i, ch in enumerate(line):
        if ch in OPENERS:
            stack.append(ch)
            continue

        if ch in CLOSERS:
            index = CLOSERS.index(ch)
            opener = stack.pop()
            if opener != OPENERS[index]:
                return (ERROR_SCORES[index], 0)

    # If we get here, there were no invalid closures, so score for missing
    # closures.
    while stack:
        opener = stack.pop()
        index = OPENERS.index(opener)
        complete_score *= 5
        complete_score += COMPLETE_SCORES[index]
    return (error_score, complete_score)


def get_total_scores(lines) -> tuple[int]:
    errors = 0
    completes = []
    for line in lines:
        a, b = get_scores(line)
        errors += a
        if b != 0:
            completes.append(b)
    completes.sort()
    complete = completes[len(completes) // 2]
    return errors, complete


def run(stream, test: bool = False):
    with timing("Both parts"):
        lines = parse(stream)
        result1, result2 = get_total_scores(lines)

    return (result1, result2)
