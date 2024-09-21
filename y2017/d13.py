"""Advent of Code 2017

Day 13: Packet Scanners

https://adventofcode.com/2017/day/13
"""
import logging  # noqa: F401

from util import timing


def get_scanner_position(depth: int, rng: int | None, time: int) -> int | None:
    """Get the position of a scanner at a given time."""
    if rng is None:
        return None
    limit = rng - 1
    cycle = limit * 2
    t = time % cycle
    if t < rng:
        return t
    return limit - 1 - (t % limit)


def is_scanner_zero(rng: int | None, time: int) -> bool:
    """Return whether the scanner is at the zero position at this time.

    If `rng` is None, that is taken to mean there is no scanner present and we
    return False.
    """
    if rng is None:
        return False
    return time % ((rng - 1) * 2) == 0


class Firewall:
    def __init__(self):
        self.scanners = {}
        self.size = 0

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            depth, rng = tuple(int(x) for x in line.split(': '))
            self.scanners[depth] = rng
            self.size = max(self.size, depth + 1)

    def get_scanner_position(self, depth: int, time: int) -> int | None:
        """Get the position of a scanner at a given time."""
        r = self.scanners.get(depth)
        return get_scanner_position(depth, r, time)

    def is_caught(self, depth: int, time: int) -> bool:
        """Return whether the packet is caught at this depth and time.

        A packet is caught if there is a scanner at this depth, and that
        scanner is in the zero position at this time.
        """
        rng = self.scanners.get(depth)
        return is_scanner_zero(rng, time)

    def get_severity(self, start: int = 0) -> set:
        """Return the total severity of passing through the firewall.

        `start` is the time value to begin at, this is the time value at which
        we will arrive at layer 0.

        Each time we are detected by a scanner, we add the scanner's depth
        multiplied by its range to the severity score.

        Once the trip is complete, return the total severity score.
        """
        depth = 0
        result = 0
        t = start
        while depth < self.size:
            if self.is_caught(depth, t):
                logging.debug(f"Caught at depth {depth}")
                result += depth * self.scanners[depth]
            depth += 1
            t += 1
        return result

    def is_safe(self, start: int = 0) -> bool:
        """Return whether the given departure time leads to a safe run.

        A safe run is one where we don't get caught by any scanner.
        """
        depth = 0
        t = start
        while depth < self.size:
            if self.is_caught(depth, t):
                logging.debug(f"Caught at depth {depth}")
                return False
            depth += 1
            t += 1
        return True

    def get_earliest_safe_time(self) -> int:
        """Find the earliest safe departure time."""
        start = 0
        while True:
            logging.debug(f"Trying with t = {start}")
            if self.is_safe(start):
                return start
            start += 1


def run(stream, test: bool = False):
    with timing("Part 1"):
        fw = Firewall()
        fw.parse(stream)
        result1 = fw.get_severity(0)

    with timing("Part 2"):
        result2 = fw.get_earliest_safe_time()

    return (result1, result2)
