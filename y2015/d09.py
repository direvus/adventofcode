from itertools import combinations, permutations


class Graph:
    """A weighted directed graph.

    The inputs are assumed to be complete graphs, so we expect there is an edge
    between every pair of nodes.
    """
    def __init__(self):
        self.nodes = set()
        self.edges = {}  # frozenset(node, node): distance
        self.maxima = {}  # num nodes: distance

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            nodes, dist = line.split(' = ')
            a, b = nodes.split(' to ')
            self.nodes |= {a, b}
            self.edges[frozenset({a, b})] = int(dist)

        dists = list(self.edges.values())
        dists.sort(reverse=True)
        self.maxima = {n: sum(dists[:n]) for n in range(1, len(self.nodes))}

    def find_shortest_path(self, a: str, b: str) -> int:
        """Find the shortest Hamiltonian path between two nodes.

        Assuming a complete graph, this works by randomly trying each possible
        ordering of the intermediate nodes between `a` and `b`. It will drop
        out early from a particular ordering if at any point the distance
        exceeds the best total path length found so far.

        Return the total distance of the shortest path.
        """
        shortest = float('inf')
        dests = list(self.nodes - {a, b})
        for nodes in permutations(dests):
            dist = 0
            prev = a
            for node in nodes:
                dist += self.edges[frozenset({node, prev})]
                if dist > shortest:
                    # No point continuing on this path
                    dist = None
                    break
                prev = node
            if dist is not None:
                dist += self.edges[frozenset({prev, b})]
                if dist < shortest:
                    shortest = dist
        return shortest

    def find_overall_shortest_path(self) -> int:
        """Find the shortest path that visits all nodes (Travelling Salesman).

        The solution can start and end at any node, as long as every node is
        visited exactly once.

        Return the total distance of the shortest path.
        """
        shortest = float('inf')
        for a, b in combinations(self.nodes, 2):
            dist = self.find_shortest_path(a, b)
            if dist < shortest:
                shortest = dist
        return shortest

    def find_longest_path(self, a: str, b: str) -> int:
        """Find the longest Hamiltonian path between two nodes.

        Assuming a complete graph, this works by randomly trying each possible
        ordering of the intermediate nodes between `a` and `b`. It will drop
        out early from a particular ordering if at any point the remaining
        number of nodes to visit cannot exceed the best total path length
        found so far.

        Return the total distance of the longest path.
        """
        best = float('-inf')
        dests = list(self.nodes - {a, b})
        for nodes in permutations(dests):
            dist = 0
            prev = a
            remain = len(nodes) + 1
            for node in nodes:
                dist += self.edges[frozenset({node, prev})]
                remain -= 1
                if self.maxima[remain] + dist < best:
                    # No point continuing on this path
                    dist = None
                    break
                prev = node
            if dist is not None:
                dist += self.edges[frozenset({prev, b})]
                if dist > best:
                    best = dist
        return best

    def find_overall_longest_path(self) -> int:
        """Find the longest path that visits all nodes.

        The solution can start and end at any node, as long as every node is
        visited exactly once.

        Return the total distance of the longest path.
        """
        best = float('-inf')
        for a, b in combinations(self.nodes, 2):
            dist = self.find_longest_path(a, b)
            if dist > best:
                best = dist
        return best


def run(stream, test=False):
    result1 = 0
    result2 = 0

    g = Graph()
    g.parse(stream)

    result1 = g.find_overall_shortest_path()
    result2 = g.find_overall_longest_path()

    return (result1, result2)
