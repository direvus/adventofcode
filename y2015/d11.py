FORBIDDEN = {105, 108, 111}
LENGTH = 8


def is_valid(value: bytearray) -> bool:
    doubles = set()
    triples = False
    for i, b in enumerate(value):
        if b in FORBIDDEN:
            return False
        if i < LENGTH - 2 and value[i + 1] == b + 1 and value[i + 2] == b + 2:
            triples = True
        if i < LENGTH - 1 and value[i + 1] == b and b not in doubles:
            doubles.add(b)
    return triples and len(doubles) >= 2


def increment_string(value: bytearray) -> None:
    i = len(value) - 1
    while i >= 0:
        ch = value[i]
        if ch == 122:
            value[i] = 97
        else:
            value[i] += 1
            return
        i -= 1


def gen_next_valid_string(value: bytearray) -> bytearray:
    valid = False
    while not valid:
        increment_string(value)
        valid = is_valid(value)
    return value


def run(stream, test=False):
    value = bytearray(stream.readline().strip(), 'ascii')

    v1 = gen_next_valid_string(value)
    result1 = v1.decode('ascii')
    result2 = gen_next_valid_string(v1).decode('ascii')

    return (result1, result2)
