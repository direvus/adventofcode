"""Advent of Code 2024

Day 4: _TITLE_

https://adventofcode.com/2024/day/4
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    return tuple(x.strip() for x in stream)


def count_word_at_position(lines, size, targets, row, col) -> int:
    result = 0
    line = lines[row]
    width = len(line)
    snip = line[col: col + size]
    if snip in targets:
        logging.debug(f'found {snip} horizontally at {row}, {col}')
        result += 1
    if row <= len(lines) - size:
        vert = ''.join(line[col] for line in lines[row: row + size])
        if vert in targets:
            logging.debug(f'found {vert} vertically at {row}, {col}')
            result += 1

        if col <= width - size:
            diag = ''.join(lines[row + i][col + i] for i in range(size))
            if diag in targets:
                logging.debug(f'found {diag} diagonally at {row}, {col}')
                result += 1
        if col >= size - 1:
            diag = ''.join(lines[row + i][col - i] for i in range(size))
            if diag in targets:
                logging.debug(f'found {diag} diagonally at {row}, {col}')
                result += 1
    return result


def count_word(lines, word) -> int:
    result = 0
    size = len(word)
    rev = ''.join(reversed(word))
    targets = {word, rev}
    for row in range(len(lines)):
        line = lines[row]
        for col in range(len(line)):
            result += count_word_at_position(lines, size, targets, row, col)
    return result


def count_x_word_at_position(lines, size, targets, row, col) -> int:
    result = 0
    a = ''.join(lines[row + i][col + i] for i in range(size))
    b = ''.join(lines[row + i][col + size - 1 - i] for i in range(size))

    if a in targets and b in targets:
        result += 1
    return result


def count_x_word(lines, word) -> int:
    result = 0
    size = len(word)
    rev = ''.join(reversed(word))
    targets = {word, rev}
    for row in range(len(lines) - size + 1):
        line = lines[row]
        for col in range(len(line) - size + 1):
            result += count_x_word_at_position(lines, size, targets, row, col)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        lines = parse(stream)
        result1 = count_word(lines, 'XMAS')

    with timing("Part 2"):
        result2 = count_x_word(lines, 'MAS')

    return (result1, result2)
