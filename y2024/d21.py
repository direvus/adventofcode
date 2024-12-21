"""Advent of Code 2024

Day 21: Keypad Conundrum

https://adventofcode.com/2024/day/21
"""
import logging  # noqa: F401

from util import timing


KEYPAD = {
        '7': {
            '8': '>',
            '9': '>>',
            '4': 'v',
            '5': '>v',
            '6': '>>v',
            '1': 'vv',
            '2': '>vv',
            '3': '>>vv',
            '0': '>vvv',
            'A': '>>vvv',
            },
        '4': {
            '7': '^',
            '8': '^>',
            '9': '^>>',
            '5': '>',
            '6': '>>',
            '1': 'v',
            '2': '>v',
            '3': '>>v',
            '0': '>vv',
            'A': '>>vv',
            },
        '1': {
            '7': '^^',
            '8': '^^>',
            '9': '^^>>',
            '4': '^',
            '5': '^>',
            '6': '^>>',
            '2': '>',
            '3': '>>',
            '0': '>v',
            'A': '>>v',
            },
        '8': {
            '7': '<',
            '9': '>',
            '4': 'v<',
            '5': 'v',
            '6': '>v',
            '1': 'vv<',
            '2': 'vv',
            '3': '>vv',
            '0': 'vvv',
            'A': '>vvv',
            },
        '5': {
            '7': '<^',
            '8': '^',
            '9': '^>',
            '4': '<',
            '6': '>',
            '1': 'v<',
            '2': 'v',
            '3': '>v',
            '0': 'vv',
            'A': '>vv',
            },
        '2': {
            '7': '<^^',
            '8': '^^',
            '9': '^^>',
            '4': '<^',
            '5': '^',
            '6': '^>',
            '1': '<',
            '3': '>',
            '0': 'v',
            'A': '>v',
            },
        '0': {
            '7': '<^^^',
            '8': '^^^',
            '9': '^^^>',
            '4': '<^^',
            '5': '^^',
            '6': '^^>',
            '1': '<^',
            '2': '^',
            '3': '^>',
            'A': '>',
            },
        '9': {
            '7': '<<',
            '8': '<',
            '4': 'v<<',
            '5': 'v<',
            '6': 'v',
            '1': 'vv<<',
            '2': 'vv<',
            '3': 'vv',
            '0': 'vvv<',
            'A': 'vvv',
            },
        '6': {
            '7': '<<^',
            '8': '^<',
            '9': '^',
            '4': '<<',
            '5': '<',
            '1': 'v<<',
            '2': 'v<',
            '3': 'v',
            '0': 'vv<',
            'A': 'vv',
            },
        '3': {
            '7': '<<^^',
            '8': '<^^',
            '9': '^^',
            '4': '<<^',
            '5': '^<',
            '6': '^',
            '1': '<<',
            '2': '<',
            '0': 'v<',
            'A': 'v',
            },
        'A': {
            '7': '<<^^^',
            '8': '<^^^',
            '9': '^^^',
            '4': '<<^^',
            '5': '<^^',
            '6': '^^',
            '1': '<<^',
            '2': '<^',
            '3': '^',
            '0': '<',
            },
        }
DIRPAD = {
        'A': {
            '^': '<',
            'v': 'v<',
            '<': 'v<<',
            '>': 'v',
            },
        '^': {
            'A': '>',
            'v': 'v',
            '<': 'v<',
            '>': '>v',
            },
        '>': {
            'A': '^',
            'v': '<',
            '<': '<<',
            '^': '^<',
            },
        '<': {
            'A': '>>^',
            'v': '>',
            '>': '>>',
            '^': '>^',
            },
        'v': {
            'A': '>^',
            '<': '<',
            '>': '>',
            '^': '^',
            },
        }


def parse(stream) -> str:
    return tuple(line.strip() for line in stream)


def get_sequence(pad: dict, code: str) -> str:
    seq = []
    position = 'A'
    for char in code:
        if position != char:
            move = pad[position][char]
        else:
            move = ''
        seq.append(move + 'A')
        logging.debug(f'{position} -> {char} = {move + "A"}')
        position = char
    logging.debug(seq)
    return ''.join(seq)


def get_nested_sequence(code: str) -> str:
    seq1 = get_sequence(KEYPAD, code)
    seq2 = get_sequence(DIRPAD, seq1)
    seq3 = get_sequence(DIRPAD, seq2)
    logging.debug(f'{code} {seq3} {len(seq3)}')
    return seq3


def get_complexity(code: str) -> int:
    num = int(code.replace('A', ''))
    return num * len(get_nested_sequence(code))


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(get_complexity(x) for x in parsed)

    with timing("Part 2"):
        result2 = 0

    return (result1, result2)
