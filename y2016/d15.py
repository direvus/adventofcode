import logging


def parse(stream) -> list:
    result = []
    for line in stream:
        words = line.split()
        size = int(words[3])
        position = int(words[-1][:-1])
        result.append((size, position))
    return result


def is_aligned(discs, t: int) -> bool:
    for i, (size, pos) in enumerate(discs):
        if (pos + i + 1 + t) % size != 0:
            return False
    return True


def get_alignment_time(discs) -> int:
    t = 0
    while not is_aligned(discs, t):
        t += 1
    return t


def run(stream, test=False, draw=False):
    discs = parse(stream)
    logging.debug(discs)

    result1 = get_alignment_time(discs)

    discs.append((11, 0))
    result2 = get_alignment_time(discs)

    return (result1, result2)
