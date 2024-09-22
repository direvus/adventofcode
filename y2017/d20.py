"""Advent of Code 2017

Day 20: Particle Swarm

https://adventofcode.com/2017/day/20
"""
import logging  # noqa: F401
from collections import namedtuple
from itertools import combinations
from operator import add

from util import timing


P3 = namedtuple('p3', ['x', 'y', 'z'])
Particle = namedtuple('particle', ['p', 'v', 'a'])


def parse(stream) -> tuple[Particle]:
    result = []
    for line in stream:
        line = line.strip()
        parts = (x[3:-1].strip() for x in line.split(', '))
        points = (P3(*[int(x) for x in y.split(',')]) for y in parts)
        particle = Particle(*points)
        result.append(particle)
    return tuple(result)


def add_points(a: P3, b: P3) -> P3:
    return P3(*map(add, a, b))


def get_distance(point: P3) -> int:
    """Get the Manhattan distance from this point to the origin."""
    return sum((abs(point.x), abs(point.y), abs(point.z)))


def get_particle_distance(particle: Particle) -> int:
    """Get the Manhattan distance from this particle to the origin."""
    return get_distance(particle.p)


def get_pair_distance(pair: set[int], particles: tuple[Particle]) -> int:
    """Get the Manhattan distance between these two particles."""
    k1, k2 = pair
    a = particles[k1]
    b = particles[k2]
    return sum((
            abs(b.p.x - a.p.x),
            abs(b.p.y - a.p.y),
            abs(b.p.z - a.p.z)))


def update_particle(p: Particle) -> Particle:
    """Return a new particle by advancing `p` by one time tick."""
    vel = add_points(p.v, p.a)
    pos = add_points(p.p, vel)
    return Particle(pos, vel, p.a)


def sign(n: int) -> int:
    if n == 0:
        return 0
    elif n > 0:
        return 1
    return -1


def has_inflection(p: Particle) -> bool:
    """Return whether the particle has an inflection in its future path.

    This is true if the sign of its acceleration differs from the sign of its
    velocity, in any axis.
    """
    return (
            (p.a.x != 0 and sign(p.a.x) != sign(p.v.x)) or
            (p.a.y != 0 and sign(p.a.y) != sign(p.v.y)) or
            (p.a.z != 0 and sign(p.a.z) != sign(p.v.z)))


def find_collisions(particles: tuple[Particle]) -> set[int]:
    """Return the indexes of all the particles that will collide.

    At each tick of time, look for any particles that occupy the same position.
    Those particles collide and are removed. For all remaining pairs of
    particles, check to see whether they are closer together now than they were
    in the last tick. If they are getting further apart, and neither of them
    have a future inflection, then we suppose that they are only going to get
    further apart as more time passes, so remove that pair from consideration.

    Keep going until either all particles have collided, or there are no more
    future collisions left to consider.

    Return the index numbers of all the particles that were found to collide.
    """
    t = 0
    remain = {i: p for i, p in enumerate(particles)}
    pairs = {frozenset(pair) for pair in combinations(remain.keys(), 2)}
    distances = {pair: get_pair_distance(pair, particles) for pair in pairs}
    inflections = {k for k, v in remain.items() if has_inflection(v)}
    collisions = set()

    while remain and pairs:
        points = set()
        collision_points = set()
        for k, p in remain.items():
            if p.p in points:
                logging.debug(f"Collision detected at {p.p}")
                collision_points.add(p.p)
            points.add(p.p)
        remove = {k for k, v in remain.items() if v.p in collision_points}
        for k in remove:
            logging.debug(f"Removing #{k}")
            del remain[k]
        collisions |= remove
        pairs = {x for x in pairs if not x & remove}

        for k, p in remain.items():
            remain[k] = update_particle(p)
            if k in inflections:
                # Let's see if it still has a future inflection
                if not has_inflection(p):
                    inflections.remove(k)

        divergent = set()
        for pair in pairs:
            prev = distances[pair]
            curr = get_pair_distance(pair, remain)
            if curr > prev and not pair & inflections:
                # Okay, these two aren't going to ever collide.
                divergent.add(pair)
            distances[pair] = curr
        pairs -= divergent

        pair_keys = set().union(*pairs)
        remove = {k for k in remain.keys() if k not in pair_keys}
        for k in remove:
            logging.debug(f"Removing #{k}, it is not in any candidate pairs")
            del remain[k]
        t += 1
    return collisions


def run(stream, test: bool = False):
    with timing("Part 1"):
        particles = parse(stream)
        dists = [
                (
                    get_distance(p.a),
                    get_distance(p.v),
                    get_distance(p.p),
                    i,
                )
                for i, p in enumerate(particles)]
        dists.sort()
        result1 = dists[0][3]

    with timing("Part 2"):
        collisions = find_collisions(particles)
        result2 = len(particles) - len(collisions)

    return (result1, result2)
