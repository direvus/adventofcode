"""Advent of Code 2017

Day 20: Particle Swarm

https://adventofcode.com/2017/day/20
"""
import logging  # noqa: F401
from collections import namedtuple
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
    return get_distance(particle.p)


def update_particle(p: Particle) -> Particle:
    """Return a new particle by advancing `p` by one time tick."""
    vel = add_points(p.v, p.a)
    pos = add_points(p.p, vel)
    return Particle(pos, vel, p.a)


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
        result2 = 0

    return (result1, result2)
