"""Advent of Code 2017

Day 7: Recursive Circus

https://adventofcode.com/2017/day/7
"""
import logging
from collections import defaultdict

from util import timing


class Tree:
    def __init__(self):
        self.nodes = {}
        self.children = defaultdict(set)
        self.parents = {}
        self.weights = {}

    def parse(self, stream):
        for line in stream:
            words = line.strip().split(maxsplit=3)
            name = words[0]
            weight = int(words[1][1:-1])
            self.nodes[name] = weight

            if len(words) > 3 and words[2] == '->':
                children = words[3].split(', ')
                for child in children:
                    self.children[name].add(child)
                    self.parents[child] = name

    def find_root(self) -> str:
        parents = set(self.children.keys())
        roots = parents - set(self.parents.keys())

        assert len(roots) == 1
        (self.root,) = tuple(roots)
        return self.root

    def get_total_weights(self) -> None:
        """Get the total weight of each node and all its descendants.

        Store the results in self.weights.
        """
        # Set each node's total weight to its own weight, then starting with
        # the leaf nodes, add the total weight of each node to the total for
        # its parent. Move up to a parent node once all of its children have
        # checked in.
        self.weights = dict(self.nodes)
        q = list(set(self.parents.keys()) - set(self.children.keys()))
        visited = set()
        while q:
            node = q.pop(0)
            parent = self.parents.get(node)
            if parent:
                weight = self.weights[node]
                self.weights[parent] += weight
                visited.add(node)
                # Have all children of this parent checked in?
                if not set(self.children[parent]) - visited:
                    q.append(parent)

    def find_imbalance(self) -> str:
        """Search the tree for an unbalanced node.

        It is a constraint of the puzzle that only one node in the tree has the
        wrong weight, so we are looking for the node whose children are
        balanced against each other, but the node is not balanced against its
        siblings.

        Return the unbalanced node's name.
        """
        self.get_total_weights()
        q = [self.root]
        while q:
            node = q.pop(0)
            weights = defaultdict(set)
            for child in self.children[node]:
                w = self.weights[child]
                weights[w].add(child)
            if len(weights.keys()) == 1:
                # All child weights are equal, so this node is the one that is
                # unbalanced with respect to its siblings.
                return node

            groups = sorted(
                    weights.items(),
                    key=lambda x: len(x[1]),
                    reverse=True)
            majority, _ = groups[0]
            minority, [target] = groups[1]
            logging.debug(
                    f"Imbalance at {node}: children have "
                    f"{dict(weights)}")
            logging.debug(f"{target} is the minority, check it next")
            q.append(target)

    def get_balanced_weight(self, node: str) -> int:
        """Return the balanced weight of the given node.

        That is the weight the node would need to be, for its total weight
        (including all descendants) to match that of its siblings.
        """
        parent = self.parents[node]
        weights = set()
        for sibling in self.children[parent]:
            if sibling == node:
                continue
            weights.add(self.weights[sibling])

        assert len(weights) == 1
        target, = tuple(weights)
        current = self.weights[node]
        diff = target - current
        return self.nodes[node] + diff


def run(stream, test=False):
    with timing("Part 1"):
        tree = Tree()
        tree.parse(stream)
        result1 = tree.find_root()
    with timing("Part 2"):
        node = tree.find_imbalance()
        result2 = tree.get_balanced_weight(node)

    return (result1, result2)
