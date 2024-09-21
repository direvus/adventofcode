"""Advent of Code 2017

Day 9: Stream Processing

https://adventofcode.com/2017/day/9
"""
import logging  # noqa: F401
from io import StringIO

from util import timing


def parse_stream(stream) -> tuple:
    """Parse the stream and return the total score and garbage count.

    The score of a group is its depth, with the top-level group having a score
    of 1, its immediate children each having a score of 2, and so on. The total
    score is the sum of the scores of all groups in the stream.

    The garbage count is the number of garbage content characters, excluding
    the `<` and `>` marking the edges of the garbage, and also excluding `!`
    escapes and the characters following those escapes.
    """
    if isinstance(stream, str):
        stream = StringIO(stream)
    depth = 0
    ch = stream.read(1)
    quoted = False
    score = 0
    count = 0
    while ch:
        logging.debug(f"{ch} with quoted = {quoted}")
        if quoted:
            match ch:
                case '!':
                    # Discard the next character
                    stream.read(1)
                case '>':
                    quoted = False
                case _:
                    count += 1
        else:
            match ch:
                case '<':
                    quoted = True
                case '{':
                    depth += 1
                case '}':
                    score += depth
                    depth -= 1
        ch = stream.read(1)
    return score, count


def get_total_score(stream) -> int:
    return parse_stream(stream)[0]


def get_garbage_count(stream) -> int:
    return parse_stream(stream)[1]


def run(stream, test: bool = False):
    with timing("Parts 1 + 2"):
        result1, result2 = parse_stream(stream)

    return (result1, result2)
