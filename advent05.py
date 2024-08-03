#!/usr/bin/env python
import sys


def resolve_map(entries: list, value: int) -> int:
    for start, end, offset in entries:
        if value >= start and value < end:
            return value + offset
    return value


def resolve_seed(maps: list, seed: int) -> int:
    v = seed
    for m in maps:
        v = resolve_map(m, v)
    return v


if __name__ == '__main__':
    seeds = []
    maps = []
    results = []
    entries = []
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        if line.startswith('seeds:'):
            seeds = [int(x) for x in line[7:].split()]
            continue
        
        if line.endswith('map:'):
            if entries:
                maps.append(entries)
            entries = []
            continue

        n = [int(x) for x in line.split()]
        if len(n) == 3:
            # (source start, source end, offset)
            entries.append((n[1], n[1] + n[2], n[0] - n[1]))

    if entries:
        maps.append(entries)

    for seed in seeds:
        results.append(resolve_seed(maps, seed))

    print(min(results))
