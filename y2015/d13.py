import re
from itertools import permutations
from rich import print


PATTERN = re.compile(
        r'(\w+) would (gain|lose) (\d+) happiness units by sitting '
        r'next to (\w+)')


class Graph:
    """A symmetric weighted graph"""
    def __init__(self):
        self.nodes = set()
        self.edges = {}  # (a, b): cost for a -> b

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PATTERN.match(line)
            if not m:
                print(f"{line} didn't match")
                continue
            a, direction, cost, b = m.groups()
            cost = int(cost)
            if direction == 'gain':
                cost = -cost
            self.nodes |= {a, b}
            self.edges[(a, b)] = cost

    def add_node(self, name: str, cost: int):
        """Add a node to the graph.

        `cost` is the cost between this node and every other existing node.
        """
        for node in self.nodes:
            self.edges[(name, node)] = cost
            self.edges[(node, name)] = cost
        self.nodes.add(name)

    def get_least_cost(self) -> int:
        """Return the cost of the least-cost arrangement.

        Check each unique ordering of all nodes for the total cost in both
        directions between each pair of adjacent nodes. The nodes are in a
        loop, so the total cost includes the costs between the final node and
        the start node.
        """
        best = float('inf')
        for nodes in permutations(self.nodes):
            cost = 0
            for i in range(len(nodes)):
                a = nodes[i]
                b = nodes[(i + 1) % len(nodes)]
                cost += self.edges[(a, b)] + self.edges[(b, a)]
            if cost < best:
                best = cost
        return best


def run(stream, test=False):
    g = Graph()
    g.parse(stream)

    result1 = -g.get_least_cost()

    g.add_node('self', 0)
    result2 = -g.get_least_cost()

    return (result1, result2)
