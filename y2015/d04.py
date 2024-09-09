import hashlib


def find_digest(prefix: str, target: str) -> int:
    h = hashlib.md5(prefix.encode('ascii'))
    length = len(target)
    digest = ''
    suffix = 0
    while digest[:length] != target:
        h2 = h.copy()
        suffix += 1
        h2.update(str(suffix).encode('ascii'))
        digest = h2.hexdigest()
    return suffix


def run(stream, test=False):
    line = stream.readline().strip()
    result1 = find_digest(line, '00000')
    result2 = find_digest(line, '000000')
    return (result1, result2)
