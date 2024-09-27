"""Advent of Code 2018

Day 8: Memory Maneuver

https://adventofcode.com/2018/day/8
"""
import logging  # noqa: F401
from collections import defaultdict

from util import timing


class Tree:
    def __init__(self):
        self.nodes = defaultdict(list)
        self.children = defaultdict(list)
        self.values = {}

    def parse(self, stream):
        line = stream.readline().strip()
        data = [int(x) for x in line.split()]
        data.reverse()

        nchild = data.pop()
        nmeta = data.pop()
        index = 0
        logging.debug(
                f"Reading root node {index} with {nchild} children "
                f"and {nmeta} meta")
        q = [(1, index, nmeta)]
        q.extend((0, index, 0) for _ in range(nchild))

        while q:
            task, parent, count = q.pop()
            if task == 0:
                # Add a child node
                index += 1
                self.children[parent].append(index)
                nchild = data.pop()
                nmeta = data.pop()
                logging.debug(
                        f"Reading new node {parent}->{index} "
                        f"with {nchild} children and {nmeta} meta")
                q.append((1, index, nmeta))
                q.extend((0, index, 0) for _ in range(nchild))

            else:
                # Add metadata
                logging.debug(f"Reading {count} metadata for {parent}")
                self.nodes[parent] = list(reversed(data[-count:]))
                data = data[:-count]

    def get_meta_sum(self):
        return sum(sum(n) for n in self.nodes.values())

    def get_node_value(self, node: int) -> int:
        if node in self.values:
            return self.values[node]
        if node not in self.children:
            # Sum this node's metadata
            result = sum(self.nodes[node])
            self.values[node] = result
            return result
        # Each meta is an index into the node's children
        result = 0
        self.children[node].sort()
        for meta in self.nodes[node]:
            if meta < 1 or meta > len(self.children[node]):
                # Skip invalid reference
                continue
            child = self.children[node][meta - 1]
            result += self.get_node_value(child)
        self.values[node] = result
        return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        tree = Tree()
        tree.parse(stream)
        result1 = tree.get_meta_sum()

    with timing("Part 2"):
        result2 = tree.get_node_value(0)

    return (result1, result2)
