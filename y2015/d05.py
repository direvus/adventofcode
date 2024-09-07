import re
import string


VOWELS = 'aeiou'
NAUGHTY = {'ab', 'cd', 'pq', 'xy'}
DOUBLES = {x + x for x in string.ascii_lowercase}
GAP_REPEAT = re.compile(r'(.).\1')
TWO_PAIR = re.compile(r'(..).*\1')


def is_nice(line: str) -> bool:
    for s in NAUGHTY:
        if s in line:
            return False
    double = False
    prev = None
    vowels = 0
    for ch in line:
        if ch == prev:
            double = True
        if ch in VOWELS:
            vowels += 1
        prev = ch
    return vowels >= 3 and double


def is_nice2(line: str) -> bool:
    return GAP_REPEAT.search(line) and TWO_PAIR.search(line)


def run(stream, test=False):
    result1 = 0
    result2 = 0
    for line in stream:
        if is_nice(line):
            result1 += 1
        if is_nice2(line):
            result2 += 1
    return (result1, result2)
