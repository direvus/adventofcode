import heapq
import math
import re
from collections import defaultdict


INF = float('inf')
ATOM = re.compile(r'[A-Z][a-z]?')


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.finder = {}
        self.deleted = set()

    def __len__(self):
        return len(self.queue)

    def __bool__(self):
        return bool(self.finder)

    def push(self, node, priority):
        entry = (priority, node)
        heapq.heappush(self.queue, entry)
        self.finder[node] = entry

    def has_node(self, node):
        return node in self.finder

    def has_position(self, position):
        return position in {(n.y, n.x) for n in self.finder.keys()}

    def set_priority(self, node, priority):
        if node in self.finder:
            self.deleted.add(id(self.finder[node]))
        self.push(node, priority)

    def pop(self):
        while self.queue:
            entry = heapq.heappop(self.queue)
            if id(entry) not in self.deleted:
                del self.finder[entry[1]]
                return entry
            self.deleted.discard(id(entry))
        raise KeyError('Cannot pop from empty priority queue')


def get_atoms(molecule: str) -> tuple[str]:
    return tuple(ATOM.findall(molecule))


def get_common_prefix_len(a, b) -> int:
    length = min(len(a), len(b))
    for i in range(length):
        if a[i] != b[i]:
            return i
    return length


def get_neighbours(
        molecule: tuple, reps: set,
        maxdiff: int = INF, prefix: int = 0) -> set[str]:
    outputs = set()
    for src, dst in reps:
        index = prefix
        diff = len(dst) - len(src)
        if diff > maxdiff:
            continue
        while src in molecule[index:]:
            index = molecule.index(src, index)
            output = molecule[:index] + dst + molecule[index + 1:]
            outputs.add(output)
            index += 1
    return outputs


def get_min_distance(start: tuple, dest: tuple, maxdiff: int) -> float:
    """Return the best-case distance between two strings."""
    diff = len(dest) - len(start)
    if diff == 0:
        return 1
    if diff < 0:
        # Replacements can't ever make the string shorter
        return INF
    return math.ceil(diff / maxdiff)


def find_path_astar(dest: tuple, reps: set, start: tuple = ('e',)) -> int:
    nodes = PriorityQueue()
    length = len(dest)
    maxdiff = max(len(b) for a, b in reps) - 1
    nodes.push(start, 1)
    origins = {}
    g = defaultdict(lambda: INF)
    g[start] = 0

    while nodes:
        cost, current = nodes.pop()
        if current == dest:
            n = current
            path = [n]
            while n in origins:
                n = origins[n]
                path.insert(0, n)
            print(path)
            return g[current]

        diff = length - len(current)
        prefix = get_common_prefix_len(current[:-1], dest)
        neighbours = get_neighbours(current, reps, diff, prefix)
        for neighbour in neighbours:
            score = g[current] + 1
            if score < g[neighbour]:
                # Best path to the neighbour so far
                origins[neighbour] = current
                g[neighbour] = score

                dist = len(current)
                fscore = score + dist
                nodes.set_priority(neighbour, fscore)
    print("Ran out of nodes without finding the destination!")


def parse(stream) -> tuple[set, tuple]:
    reps = set()
    for line in stream:
        line = line.strip()
        if not line:
            break
        a, b = line.split(' => ')
        reps.add((a, get_atoms(b)))
    target = get_atoms(stream.readline().strip())
    return reps, target


def count_outputs(reps: set, molecule: tuple) -> int:
    outputs = get_neighbours(molecule, reps)
    return len(outputs)


def run(stream, test=False, draw=False):
    reps, molecule = parse(stream)
    result1 = count_outputs(reps, molecule)
    result2 = find_path_astar(molecule, reps)
    return (result1, result2)
