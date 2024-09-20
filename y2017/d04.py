"""Advent of Code 2017

Day 4: High-Entropy Passphrases

https://adventofcode.com/2017/day/4
"""
import logging


def parse(stream) -> tuple:
    return tuple(line.strip().split() for line in stream)


def count_valid_passphrases(passphrases: tuple) -> int:
    result = 0
    for phrase in passphrases:
        if len(set(phrase)) == len(phrase):
            result += 1
    return result


def count_valid_passphrases_p2(passphrases: tuple) -> int:
    result = 0
    for phrase in passphrases:
        if len(set(phrase)) != len(phrase):
            logging.debug(f"{phrase} has reused words")
            continue
        if len({tuple(sorted(word)) for word in phrase}) != len(phrase):
            logging.debug(f"{phrase} has anagrams")
            continue
        result += 1
    return result


def run(stream, test=False):
    passphrases = parse(stream)
    result1 = count_valid_passphrases(passphrases)
    result2 = count_valid_passphrases_p2(passphrases)

    return (result1, result2)
