"""Advent of Code 2024

Day 5: Print Queue

https://adventofcode.com/2024/day/5
"""
import logging  # noqa: F401

from util import timing


def parse(stream) -> str:
    rules = []
    productions = []

    for line in stream:
        if line.strip() == '':
            break
        rules.append(tuple(map(int, line.split('|'))))

    for line in stream:
        productions.append(tuple(map(int, line.split(','))))

    return rules, productions


def is_valid(production, rules) -> bool:
    """Return whether a production complies with all rules."""
    for i, page in enumerate(production):
        for a, b in rules:
            if page == a and b in production:
                # Then `b` must appear later.
                if production.index(b) < i:
                    return False
            elif page == b and a in production:
                # Then `a` must appear earlier.
                if production.index(a) > i:
                    return False
    return True


def get_middle_page(production) -> int:
    return production[len(production) // 2]


def get_valid_middle_pages(rules, productions) -> list:
    result = [get_middle_page(x) for x in productions if is_valid(x, rules)]
    return result


def fix_pass(production, rules) -> bool:
    """Perform a single pass of attempting to fix a production.

    The first time we encounter a pair of pages that are incorrectly ordered,
    we will swap them around by mutating the `production` list directly, and
    then return True to indicate the list was changed.

    If we get to the end of the list without making any changes, return False.
    """
    for i, page in enumerate(production):
        for a, b in rules:
            if page == a and b in production:
                # Then `b` must appear later.
                j = production.index(b)
                if j < i:
                    production[i] = b
                    production[j] = a
                    return True

            elif page == b and a in production:
                # Then `a` must appear earlier.
                j = production.index(a)
                if j > i:
                    production[i] = a
                    production[j] = b
                    return True
    return False


def fix(production, rules) -> tuple:
    result = list(production)
    changed = True
    while changed:
        changed = fix_pass(result, rules)
    return tuple(result)


def get_corrected_middle_pages(rules, productions) -> list:
    result = [get_middle_page(fix(x, rules)) for x in productions if not is_valid(x, rules)]
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        parsed = parse(stream)
        result1 = sum(get_valid_middle_pages(*parsed))

    with timing("Part 2"):
        result2 = sum(get_corrected_middle_pages(*parsed))

    return (result1, result2)
