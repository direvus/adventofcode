#!/usr/bin/env python
import sys


if __name__ == '__main__':
    line = sys.stdin.readline().strip()
    trans = str.maketrans('LR', '01')
    directions = tuple(int(x) for x in line.translate(trans))
    net = {}
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        k = line[:3]
        l = line[7:10]
        r = line[12:15]
        net[k] = (l, r)

    # Part 1
    try:
        node = 'AAA'
        steps = 0
        dircount = len(directions)
        while node != 'ZZZ':
            direction = directions[steps % dircount]
            node = net[node][direction]
            steps += 1
        print(steps)
    except KeyError:
        print(f"No node AAA, cannot complete Part 1.")

    # Part 2
    nodes = [x for x in net.keys() if x.endswith('A')]
    steps = 0
    while set([x[-1] for x in nodes]) != {'Z'}:
        direction = directions[steps % dircount]
        newnodes = []
        for node in nodes:
            newnodes.append(net[node][direction])
        nodes = newnodes
        steps += 1
    print(steps)
