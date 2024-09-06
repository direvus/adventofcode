#!/usr/bin/env python
import sys


def get_race_ways(time: int, distance: int) -> int:
    """Return the number of ways to win the race."""
    count = 0
    for i in range(1, time):
        if (time - i) * i > distance:
            count += 1
    return count


if __name__ == '__main__':
    times = []
    distances = []
    for line in sys.stdin:
        line = line.strip()
        if line.startswith('Time:'):
            parts = line[6:].strip().split()
            times = [int(x) for x in parts]
            time2 = int(''.join(parts))
            continue

        if line.startswith('Distance:'):
            parts = line[10:].strip().split()
            distances = [int(x) for x in parts]
            distance2 = int(''.join(parts))

    total = 1
    for i, time in enumerate(times):
        dist = distances[i]
        ways = get_race_ways(time, dist)
        print(f"Race {i + 1} has {ways} ways to win")
        total *= ways
    print(total)

    ways = get_race_ways(time2, distance2)
    print(f"Part 2 race has {ways} to win")
