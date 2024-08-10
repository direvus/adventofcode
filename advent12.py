#!/usr/bin/env python
import re
import sys


def replace(source: str, position: int, replacement: str):
    return source[:position] + replacement + source[position + 1:]


def build_regex(runs: tuple[int]) -> re.Pattern:
    run_pattern = r'[.?]+'.join([f'[#?]{{{x}}}' for x in runs])
    return re.compile(r'[.?]*' + run_pattern + r'[.?]*')


def simplify(row: str, regex: re.Pattern) -> str:
    indexes = [i for i, x in enumerate(row) if x == '?']
    for i in indexes:
        with_hash = replace(row, i, '#')
        with_dot = replace(row, i, '.')
        hash_ok = regex.fullmatch(with_hash)
        dot_ok = regex.fullmatch(with_dot)

        if dot_ok and not hash_ok:
            row = with_dot
        if hash_ok and not dot_ok:
            row = with_hash
    return row


def get_ways(
        row: str,
        runs: tuple[int],
        regex: re.Pattern = None,
        ) -> list[str]:
    if not regex:
        regex = build_regex(runs)
    indexes = [i for i, x in enumerate(row) if x == '?']
    unknown = len(indexes)
    total = sum(runs)
    missing = total - row.count('#')
    if unknown == 0:
        return [row]
    if missing == unknown:
        return [row.replace('?', '#')]

    i = indexes[0]
    result = []
    for ch in ('#', '.'):
        attempt = replace(row, i, ch)
        valid = regex.fullmatch(attempt)
        if valid:
            result.extend(get_ways(attempt, runs, regex))
    return result


if __name__ == '__main__':
    rows = []
    for line in sys.stdin:
        field, runs = line.strip().split()
        runs = tuple([int(x) for x in runs.split(',')])
        rows.append([field, runs])

    # Part 1
    total = 0
    part1 = []
    for row, runs in rows:
        regex = build_regex(runs)
        simple = simplify(row, regex)
        nways = len(get_ways(simple, runs, regex))
        total += nways
        part1.append(nways)
    print(total)

    # Part 2
    #
    # We already know all the ways the expanded row can be solved WITHOUT using
    # the new '?' delimiters - we just need to check all the ways it can be
    # solved where we do use at least one of them.
    total = 0
    for i, nways in enumerate(part1):
        origrow, runs = rows[i]

        joins = []
        for n in range(2, 6):
            row = '#'.join([origrow] * n)
            subruns = runs * n
            regex = build_regex(subruns)
            if not regex.fullmatch(row):
                joins.append(0)
                continue
            simple = simplify(row, regex)
            joins.append(len(get_ways(simple, subruns, regex)))

        subtotal = sum([
                nways ** 5,
                4 * joins[0] * (nways ** 3),
                3 * joins[1] * (nways ** 2),
                2 * joins[2] * nways,
                3 * (joins[0] ** 2) * nways,
                2 * joins[0] * joins[1],
                joins[3],
                ])
        print(f"R{i + 1} = {subtotal}")
        total += subtotal
    print(total)
