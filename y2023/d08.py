#!/usr/bin/env python
import math


def run(stream, test=False):
    line = stream.readline().strip()
    trans = str.maketrans('LR', '01')
    directions = tuple(int(x) for x in line.translate(trans))
    net = {}
    for line in stream:
        line = line.strip()
        if line == '':
            continue
        k = line[:3]
        left = line[7:10]
        right = line[12:15]
        net[k] = (left, right)

    dircount = len(directions)
    # Part 1
    try:
        node = 'AAA'
        steps = 0
        while node != 'ZZZ':
            direction = directions[steps % dircount]
            node = net[node][direction]
            steps += 1
        p1 = steps
    except KeyError:
        print("No node AAA, cannot complete Part 1.")

    # Part 2
    nodes = [x for x in net.keys() if x.endswith('A')]
    steps = 0
    cycles = [None] * len(nodes)
    while None in cycles:
        direction = directions[steps % dircount]
        steps += 1
        for i, node in enumerate(nodes):
            new = net[node][direction]
            nodes[i] = new
            if new[2] == 'Z' and cycles[i] is None:
                cycles[i] = steps
    p2 = math.lcm(*cycles)
    return (p1, p2)
