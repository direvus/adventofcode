import hashlib


def parse(stream) -> list:
    for line in stream:
        line = line.strip()
        return line


def get_password(door: str) -> str:
    result = []
    i = 0
    base = hashlib.md5(door.encode('ascii'))
    while len(result) < 8:
        h = base.copy()
        h.update(str(i).encode('ascii'))
        digest = h.hexdigest()
        if digest.startswith('00000'):
            result.append(digest[5])
        i += 1
    return ''.join(result)


def run(stream, test=False, draw=False):
    door = parse(stream)

    result1 = get_password(door)
    result2 = 0

    return (result1, result2)
