"""matrix.py

Utility module for matrix operations
"""
from fractions import Fraction


def num_leading_zeros(row: list) -> int:
    for i, n in enumerate(row):
        if n != 0:
            return i
    return i + 1


def get_non_echelon_row(matrix: list) -> int:
    prev = -1
    for i, row in enumerate(matrix):
        z = num_leading_zeros(row)
        if z == len(row):
            return None
        if z <= prev:
            return i
        prev = z
    return None


def scale_iter(v, f):
    return tuple((x * f for x in v))


def solve_gaussian(matrix: list) -> list:
    """Perform a Gaussian elimination on an augmented matrix.

    Return the list of values in the solution as Fractions.
    """
    while True:
        matrix.sort(key=num_leading_zeros)
        i = get_non_echelon_row(matrix)
        if i is None:
            break
        j = num_leading_zeros(matrix[i])
        upper = matrix[i - 1]
        for i in range(i, len(matrix)):
            lead = matrix[i][j]
            if lead == 0:
                break
            factor = Fraction(0 - lead, upper[j])
            scaled = scale_iter(upper, factor)
            matrix[i] = tuple(map(lambda a, b: a + b, matrix[i], scaled))

    width = len(matrix[0]) - 1
    solution = [None] * width
    for row in reversed(matrix):
        z = num_leading_zeros(row)
        if z >= width:
            continue
        aug = row[width]
        for j in range(z + 1, width):
            if solution[j] is not None:
                aug -= row[j] * solution[j]
        solution[z] = Fraction(aug, row[z])
    return solution
