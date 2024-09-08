from itertools import combinations, product
from operator import mul


def parse(stream) -> list[int]:
    result = []
    for line in stream:
        line = line.strip()
        result.append(int(line))
    return result


def count_combinations(
        quantity: int, containers: list[int]) -> tuple[int, int]:
    """Count the number of combinations of containers that fit the quantity.

    Return a tuple of 2 integers. The first is the number of ways we can select
    some number of containers from a pool of containers such that the total
    capacity is exactly equal to the target quantity.

    The second integer in the return tuple is the smallest number of containers
    that were found to satisfy the condition.
    """
    prods = product(range(2), repeat=len(containers))
    filt = filter(lambda x: sum(map(mul, x, containers)) == quantity, prods)
    mincount = float('inf')
    combos = 0
    for nums in filt:
        combos += 1
        count = sum(nums)
        if count < mincount:
            mincount = count
    return combos, mincount


def count_num(quantity: int, containers: list[int], count: int) -> int:
    """Count the number of fitting combinations of `count` containers.

    Return an integer that is the number of ways we can select `count`
    containers from a pool of containers, such that the total capacity is
    exactly equal to `quantity`.
    """
    combos = combinations(containers, count)
    filt = filter(lambda x: sum(x) == quantity, combos)
    return sum(1 for _ in filt)


def run(stream, test=False):
    qty = 25 if test else 150
    containers = parse(stream)
    result1, mincount = count_combinations(qty, containers)
    result2 = count_num(qty, containers, mincount)
    return (result1, result2)
