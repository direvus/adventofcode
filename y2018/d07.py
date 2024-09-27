"""Advent of Code 2018

Day 7: _TITLE_

https://adventofcode.com/2018/day/7
"""
import logging  # noqa: F401
from collections import defaultdict
from graphlib import TopologicalSorter

from util import timing


class Graph:
    def __init__(self):
        self.nodes = defaultdict(set)
        self.deps = defaultdict(set)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            words = line.split()
            source = words[1]
            dest = words[7]
            self.nodes[source].add(dest)
            self.deps[dest].add(source)

    def get_topo(self):
        topo = TopologicalSorter(self.deps)
        topo.prepare()
        result = []
        q = []
        while topo.is_active() or q:
            nodes = topo.get_ready()
            q.extend(nodes)
            q.sort()
            node = q.pop(0)
            result.append(node)
            topo.done(node)
        return tuple(result)

    def get_time(self, workers: int, lead: int) -> int:
        """Return the total time taken to complete all tasks."""
        topo = TopologicalSorter(self.deps)
        topo.prepare()
        time = 0
        work = {}
        q = []
        q.extend(sorted(topo.get_ready()))
        idle = set(range(workers))

        while q or topo.is_active() or work:
            # Assign queued tasks to idle workers
            while q and idle:
                task = q.pop(0)
                w = idle.pop()
                logging.debug(f"At t = {time}, {task} to idle worker {w}")
                timer = ord(task) - ord('A') + lead + 1
                work[w] = (task, timer)

            # Progress tasks
            keys = tuple(work.keys())
            for w in keys:
                task, timer = work[w]
                timer -= 1
                if timer == 0:
                    logging.debug(f"Worker {w} has completed {task}")
                    del work[w]
                    idle.add(w)
                    topo.done(task)
                else:
                    work[w] = (task, timer)

            # If new tasks are ready, queue them up
            q.extend(sorted(topo.get_ready()))
            time += 1
        return time


def run(stream, test: bool = False):
    with timing("Part 1"):
        g = Graph()
        g.parse(stream)
        result1 = ''.join(g.get_topo())

    with timing("Part 2"):
        workers = 2 if test else 5
        lead = 0 if test else 60
        result2 = g.get_time(workers, lead)

    return (result1, result2)
