import math
from itertools import product


def parse(stream) -> tuple:
    packages = []
    for line in stream:
        weight = int(line.strip())
        packages.append(weight)
    return tuple(packages)


def get_entanglement(packages: tuple) -> int:
    return math.prod(packages)


def find_best_config(packages: tuple) -> tuple:
    ids = (0, 1, 2)
    best_count = float('inf')
    best_groups = None
    best_entanglement = float('inf')
    for opt in product(ids, repeat=len(packages)):
        groups = [[], [], []]
        for i, pack in enumerate(packages):
            groups[opt[i]].append(pack)
        sums = {sum(x) for x in groups}
        if len(sums) != 1:
            # Unequal sums, discard this option
            continue
        groups.sort(key=lambda x: len(x))
        count = len(groups[0])
        if count < best_count:
            best_count = count
            best_groups = groups
            best_entanglement = get_entanglement(groups[0])
        elif count == best_count:
            ent = get_entanglement(groups[0])
            if ent < best_entanglement:
                best_groups = groups
                best_entanglement = ent
    return best_groups


def run(stream, test=False, draw=False):
    packages = parse(stream)

    conf = find_best_config(packages)
    result1 = get_entanglement(conf[0])
    result2 = 0

    return (result1, result2)
