import math
from functools import cache
from itertools import combinations


def parse(stream) -> set:
    packages = set()
    for line in stream:
        weight = int(line.strip())
        packages.add(weight)
    return packages


def get_entanglement(packages: tuple) -> int:
    return math.prod(packages)


def partitions(numbers: set, target: int):
    """Yield all the ways a partition of `target` can be made using `numbers`.

    A partition is a set of numbers that sum to the target. This function
    returns all the possible partitions of the target that can be created only
    drawing numbers from the `numbers` set, and only using each number at most
    once.

    We assume that the target and all of the numbers are positive integers.

    If `length` is set, we will only return partitions that have exactly that
    number of elements.

    This is a generator function that yields each valid partition, one at a
    time as a frozenset set, as it is found.
    """
    q = [set()]
    results = set()
    total = sum(numbers)
    while q:
        selection = q.pop(0)
        total = sum(selection)
        if total == target:
            output = frozenset(selection)
            if output not in results:
                yield selection
                results.add(output)
            continue
        if total > target:
            continue
        remain = target - total
        for n in numbers - selection:
            if n <= remain:
                q.append(selection | {n})


def length_partitions(numbers: set, target: int, length: int):
    """Yield length-restricted partitions of `target`.

    This function returns all the ways a partition of `target` can be made
    using exactly `length` distinct numbers, chosen from `numbers`.

    We assume that the target and all of the numbers are positive integers.

    This is a generator function that yields valid partitions as they are
    found.
    """
    for com in combinations(numbers, length):
        total = sum(com)
        if total != target:
            continue
        yield frozenset(com)


@cache
def has_partition(numbers: set, target: int) -> bool:
    """Return whether any partition exists of `target` from `numbers`.

    This function returns True if there is a way to select distinct numbers
    from `numbers` that sum to `target`, and False otherwise.
    """
    total = sum(numbers)
    if total < target:
        return False
    if total == target:
        return True
    if target in numbers:
        return True
    for k in range(2, len(numbers) // 2):
        for com in combinations(numbers, k):
            if sum(com) == target:
                return True
    return False


def find_best_config(packages: set, bins: int = 3) -> tuple:
    best_group = None
    best_entanglement = float('inf')
    total_weight = sum(packages)
    target = total_weight / bins
    length = 0
    while best_group is None:
        length += 1
        for primary in length_partitions(packages, target, length):
            other = frozenset(packages - primary)
            if not has_partition(other, target):
                # There's no way to actually arrange these packages evenly into
                # two groups.
                continue

            if best_group is None:
                best_group = primary
                best_entanglement = get_entanglement(primary)
            else:
                ent = get_entanglement(primary)
                if ent < best_entanglement:
                    best_group = primary
                    best_entanglement = ent
    return best_group


def run(stream, test=False, draw=False):
    packages = parse(stream)

    conf = find_best_config(packages)
    result1 = get_entanglement(conf)

    conf = find_best_config(packages, 4)
    result2 = get_entanglement(conf)

    return (result1, result2)
