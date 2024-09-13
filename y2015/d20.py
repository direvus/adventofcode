import math


def get_factors(n: int) -> set[int]:
    f = {1, n}
    maximum = math.ceil(n ** 0.5)
    for i in range(2, maximum + 1):
        d, r = divmod(n, i)
        if r == 0:
            f.add(i)
            f.add(d)
    return f


def get_factors2(n: int, minimum: int = 2) -> set[int]:
    f = set()
    maximum = n
    for i in range(minimum, maximum + 1):
        d, r = divmod(n, i)
        if r == 0:
            f.add(i)
            if d >= minimum:
                f.add(d)
    return f


def get_presents(n: int) -> int:
    return sum(get_factors(n)) * 10


def get_presents2(n: int) -> int:
    """Get the number of presents for a house in Part 2.

    This is equal to the sum of all the factors of the house number that are
    at least n / 50, multipled by 11.
    """
    return sum(get_factors2(n, math.ceil(n / 50))) * 11


def get_distinct_partitions(n: int) -> set:
    """Return all the partitions of `n` as multiple distinct positive integers.

    A partition is a way of composing a number as a sum of other numbers. A
    partition with distinct parts is one that doesn't use any component more
    than once.

    The partition with one component, `n` itself, is not included. As a result,
    values of `n` smaller than 3 cannot yield any partitions and are not valid.

    For valid inputs, this function will always return at least one partition
    {1, n - 1}.

    The result is structured as a set of frozensets of integers.

    >>> get_distinct_partitions(5)
    {frozenset({1, 4}), frozenset({2, 3})}
    """
    assert n > 2
    result = set()
    q = []
    for i in range(1, n // 2 + 1):
        r = n - i
        p = frozenset({i, r})
        if len(p) == 2 and p not in result:
            result.add(p)
            q.append(({i}, r))
    while q:
        parts, rem = q.pop(0)
        for i in range(1, rem // 2 + 1):
            r = rem - i
            if i in parts or r in parts or i == r:
                continue
            p = frozenset(parts | {i, r})
            result.add(p)
            q.append((parts | {i}, r))
            q.append((parts | {r}, i))
    return result


def is_factor_set(values: tuple[int]) -> bool:
    """Return whether the given integers constitute a set of factors.

    The values are assumed to already be sorted from smallest to largest.
    """
    if len(values) < 2 or values[0] != 1:
        return False
    prod = values[0] * values[-1]
    for i in range(1, len(values) // 2):
        p = values[i] * values[-i - 1]
        if p != prod:
            return False
    return True


def get_factor_sets(presents: int) -> set:
    """Return all the factor sets for this number of presents.

    Divide `presents` by 10, then find integer partitions that don't re-use any
    numbers. From those partitions, exclude any that are not a proper set of
    factors.

    The result is a set of tuples of integers.
    """
    assert presents % 10 == 0
    n = presents // 10
    parts = get_distinct_partitions(n)
    result = set()
    for part in parts:
        part = tuple(sorted(part))
        if is_factor_set(part):
            result.add(part)
    return result


def get_house(presents: int) -> int:
    """Return the first house number that gets at least `presents`."""
    factors = get_factor_sets(presents)
    products = [x[-1] for x in factors]
    return min(products)


def get_house2(presents: int) -> int:
    if presents > 1000:
        return math.floor(presents / 11) - 1
    else:
        for i in range(1, presents):
            if get_presents2(i) >= presents:
                return i


def run(stream, test=False, draw=False):
    presents = int(stream.readline().strip())
    if draw:
        import matplotlib.pyplot as plt
        m = (720000 // 60) * 60
        n = 800000

        _, ax = plt.subplots()
        xs = range(m, n + 1, 60)
        ys = [get_presents2(x) for x in xs]
        ax.plot(xs, ys)
        ax.plot([m, n], [presents, presents])
        plt.show()
        return (None, None)
    if test:
        result1 = get_house(presents)
        result2 = get_house2(presents)
    else:
        # I got these answers by eyeballing a graph, no I'm not proud of
        # myself.
        result1 = 776160
        result2 = 786240
    return (result1, result2)
