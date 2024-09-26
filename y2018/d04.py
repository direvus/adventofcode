"""Advent of Code 2018

Day 4: Repose Record

https://adventofcode.com/2018/day/4
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing, NINF


class Sleep:
    guard: int
    year: int
    month: int
    day: int
    start: int
    end: int

    def __init__(
            self, guard: int, year: int, month: int, day: int,
            start: int, end: int):
        self.guard = guard
        self.year = year
        self.month = month
        self.day = day
        self.start = start
        self.end = end

    @property
    def length(self) -> int:
        return self.end - self.start

    def contains(self, minute: int) -> bool:
        return minute >= self.start and minute < self.end


def parse(stream) -> tuple:
    lines = []
    for line in stream:
        lines.append(line.strip())
    lines.sort()

    result = defaultdict(list)
    guard = None
    for line in lines:
        timestamp, comment = line[1:17], line[19:]
        date, time = timestamp.split(' ')
        year, month, day = (int(x) for x in date.split('-'))
        hour, minute = (int(x) for x in time.split(':'))
        words = comment.split(' ')
        match words[0].lower():
            case 'guard':
                guard = int(words[1][1:])
            case 'falls':
                start = minute
            case 'wakes':
                end = minute
                sleep = Sleep(guard, year, month, day, start, end)
                result[guard].append(sleep)
    return result


def find_sleepiest_guard(records: dict) -> int | None:
    most = NINF
    result = None
    for guard in records:
        total = sum(x.length for x in records[guard])
        if total > most:
            most = total
            result = guard
    return result


def get_sleepiest_minute(records: dict, guard: int) -> int | None:
    sleeps = records[guard]
    most = NINF
    result = None
    for minute in range(60):
        total = sum(int(x.contains(minute)) for x in sleeps)
        if total > most:
            most = total
            result = minute
    return result


def find_highest_freq_sleep(records: dict) -> tuple | None:
    most = NINF
    result = None
    for guard, sleeps in records.items():
        for minute in range(60):
            total = sum(int(x.contains(minute)) for x in sleeps)
            if total > most:
                most = total
                result = (guard, minute)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        records = parse(stream)
        guard = find_sleepiest_guard(records)
        logging.debug(f"Guard {guard} has most minutes asleep")
        minute = get_sleepiest_minute(records, guard)
        logging.debug(f"Was most often asleep at minute {minute}")
        result1 = minute * guard

    with timing("Part 2"):
        guard, minute = find_highest_freq_sleep(records)
        logging.debug(
                f"Guard {guard} was asleep at minute {minute} more often "
                "than any other guard and minute")
        result2 = guard * minute

    return (result1, result2)
