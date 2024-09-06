#!/usr/bin/env python
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


def resolve_map_range(entries: list, start: int, size: int) -> list:
    results = []
    end = start + size
    for mapstart, mapend, offset in entries:
        if mapstart >= end or mapend <= start:
            # No overlap
            continue
        if mapstart <= start and mapend >= end:
            # Nice, the whole range fits within this entry
            results.append((start + offset, size))
            size = 0
            break
        # OK we have to split up the range
        if start < mapstart:
            count = mapstart - start
            results.append((start, count))
            start = mapstart
            size -= count

        count = min(mapend - start, size)
        results.append((start + offset, count))
        start = mapend
        size -= count
    if size:
        results.append((start, size))
    return results


def resolve_map_ranges(entries: list, ranges: list) -> int:
    results = []
    for start, size in ranges:
        results.extend(resolve_map_range(entries, start, size))
    return results


def resolve_seed_range(maps: list, start: int, size: int) -> int:
    ranges = [(start, size)]
    for m in maps:
        ranges = resolve_map_ranges(m, ranges)
    return min([x for x, y in ranges])


def run(stream, test=False):
    seeds = []
    maps = []
    entries = []
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        if line.startswith('seeds:'):
            seeds = [int(x) for x in line[7:].split()]
            continue

        if line.endswith('map:'):
            if entries:
                maps.append(sorted(entries, key=lambda x: x[0]))
            entries = []
            continue

        n = [int(x) for x in line.split()]
        if len(n) == 3:
            # (source start, source end, offset)
            entries.append((n[1], n[1] + n[2], n[0] - n[1]))

    if entries:
        maps.append(sorted(entries, key=lambda x: x[0]))

    lowest = None
    for seed in seeds:
        result = resolve_seed(maps, seed)
        if lowest is None or result < lowest:
            lowest = result
    p1 = lowest

    # Part 2: seeds are in (start, range) pairs
    lowest = None
    for i in range(0, len(seeds), 2):
        seed = seeds[i]
        size = seeds[i + 1]
        result = resolve_seed_range(maps, seed, size)
        if lowest is None or result < lowest:
            lowest = result
    p2 = lowest
    return (p1, p2)
