"""Advent of Code 2020

Day 4: Passport Processing

https://adventofcode.com/2020/day/4
"""
import logging  # noqa: F401
import re

from util import timing


REQUIRED = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
FOUR_DIGITS = re.compile(r'^\d{4}$')
NINE_DIGITS = re.compile(r'^\d{9}$')
HEIGHT_EXPR = re.compile(r'^\d+(cm|in)$')
HAIR_COLOUR = re.compile(r'^#[a-f0-9]{6}$')
EYE_COLOURS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def parse(stream) -> str:
    result = []
    entry = {}
    for line in stream:
        line = line.strip()
        if line == '':
            result.append(entry)
            entry = {}
        words = line.split()
        for word in words:
            k, v = word.split(':')
            entry[k] = v
    if entry:
        result.append(entry)
    return result


def is_valid(passport: dict) -> bool:
    for req in REQUIRED:
        if req not in passport:
            return False
    return True


def is_valid2(passport: dict) -> bool:
    if not is_valid(passport):
        return False

    if not (
            FOUR_DIGITS.fullmatch(passport['byr']) and
            FOUR_DIGITS.fullmatch(passport['iyr']) and
            FOUR_DIGITS.fullmatch(passport['eyr']) and
            HEIGHT_EXPR.fullmatch(passport['hgt']) and
            HAIR_COLOUR.fullmatch(passport['hcl']) and
            NINE_DIGITS.fullmatch(passport['pid'])):
        return False

    byr = int(passport['byr'])
    if byr < 1920 or byr > 2002:
        return False

    iyr = int(passport['iyr'])
    if iyr < 2010 or iyr > 2020:
        return False

    eyr = int(passport['eyr'])
    if eyr < 2020 or eyr > 2030:
        return False

    height = int(passport['hgt'][:-2])
    unit = passport['hgt'][-2:]
    match unit:
        case 'in':
            if height < 59 or height > 76:
                return False
        case 'cm':
            if height < 150 or height > 193:
                return False

    if passport['ecl'] not in EYE_COLOURS:
        return False

    return True


def count_valid(passports: list[dict]) -> int:
    result = 0
    for p in passports:
        result += int(is_valid(p))
    return result


def count_valid2(passports: list[dict]) -> int:
    result = 0
    for p in passports:
        result += int(is_valid2(p))
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        passports = parse(stream)
        result1 = count_valid(passports)

    with timing("Part 2"):
        result2 = count_valid2(passports)

    return (result1, result2)
