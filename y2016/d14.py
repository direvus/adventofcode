import logging
import re
from collections import defaultdict
from _md5 import md5


TRIPLES = re.compile(r'(.)\1\1')
QUINTUPLES = re.compile(r'(.)\1\1\1\1')


def parse(stream) -> list:
    return stream.readline().strip()


def stretch_key(digest: str, count: int) -> str:
    for _ in range(count):
        digest = md5(digest.encode('ascii')).hexdigest()
    return digest


def get_index(salt: bytes, keys: int, stretch: int = 0) -> int:
    found = []
    triples = defaultdict(set)
    index = 0
    base = md5(salt)
    while len(found) < keys:
        h = base.copy()
        h.update(str(index).encode('ascii'))
        digest = h.hexdigest()
        if stretch > 0:
            digest = stretch_key(h.hexdigest(), stretch)

        m = TRIPLES.search(digest)
        if m:
            t = m.group(1)
            m = QUINTUPLES.search(digest)
            if m:
                q = m.group(1)
                prev = (
                        x for x in triples[q]
                        if x >= index - 1000 and x < index)
                found.extend(prev)
                logging.debug(f"Found {m.group(0)} at index {index}")
                logging.debug(f"Total keys found now = {found}")
            triples[t].add(index)
        index += 1
    return sorted(found)[keys - 1]


def run(stream, test=False, draw=False):
    salt = parse(stream).encode('ascii')

    result1 = get_index(salt, 64)
    result2 = get_index(salt, 64, 2016)

    return (result1, result2)
