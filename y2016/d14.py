import json
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


def get_index(
        salt: bytes,
        keys: int,
        stretch: int = 0,
        md5cache: dict = None,
        stretch_cache: dict = None,
        ) -> int:
    found = []
    triples = defaultdict(set)
    index = 0
    base = md5(salt)
    saltstr = salt.decode('ascii')
    while len(found) < keys:
        k = saltstr + str(index)
        if md5cache and k in md5cache:
            digest = md5cache[k]
        else:
            h = base.copy()
            h.update(str(index).encode('ascii'))
            digest = h.hexdigest()
            if md5cache is not None:
                md5cache[k] = digest

        if stretch > 0:
            initial = digest
            if stretch_cache and initial in stretch_cache:
                digest = stretch_cache[initial]
            else:
                digest = stretch_key(initial, stretch)
                if stretch_cache is not None:
                    stretch_cache[initial] = digest

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

    stretch = 2016
    md5_cache_name = 'out/md5.json'
    stretch_cache_name = f'out/md5_stretch{stretch}.json'
    try:
        with open(md5_cache_name, 'r') as fp:
            md5cache = json.load(fp)
    except FileNotFoundError:
        md5cache = {}

    try:
        with open(stretch_cache_name, 'r') as fp:
            stretch_cache = json.load(fp)
    except FileNotFoundError:
        stretch_cache = {}

    result1 = get_index(salt, 64, md5cache=md5cache)
    result2 = get_index(
            salt, 64, 2016, md5cache=md5cache, stretch_cache=stretch_cache)

    with open(md5_cache_name, 'w') as fp:
        json.dump(md5cache, fp, separators=(',', ':'))
    with open(stretch_cache_name, 'w') as fp:
        json.dump(stretch_cache, fp, separators=(',', ':'))

    return (result1, result2)
