import hashlib


def digest(prefix: str, suffix: int) -> str:
    h = hashlib.md5(f'{prefix}{suffix}'.encode('ascii'))
    return h.hexdigest()


def run(stream, test=False):
    line = stream.readline().strip()
    suffix = 0
    while not digest(line, suffix).startswith('00000'):
        suffix += 1
    result1 = suffix

    suffix = 0
    while not digest(line, suffix).startswith('000000'):
        suffix += 1
    result2 = suffix
    return (result1, result2)
