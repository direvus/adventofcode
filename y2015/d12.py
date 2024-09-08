import json


def get_non_red_sum(obj: dict | list) -> int:
    """Get the sum of integers from a nested structure, avoiding reds.

    Traverse the tree of objects recursively, accumulating all the integers
    found.

    For any dict that has a value of 'red' for any of its keys, we ignore the
    entire dict and all of its descendants.

    Return the final sum of all integers found in this way.
    """
    if isinstance(obj, list):
        return sum([get_non_red_sum(x) for x in obj])
    elif isinstance(obj, dict):
        values = obj.values()
        if 'red' not in values:
            return sum([get_non_red_sum(x) for x in values])
    elif isinstance(obj, int):
        return obj
    return 0


def run(stream, test=False):
    result1 = 0

    def parse_int_hook(v: str) -> int:
        nonlocal result1
        i = int(v)
        result1 += i
        return i

    obj = json.load(stream, parse_int=parse_int_hook)
    result2 = get_non_red_sum(obj)

    return (result1, result2)
