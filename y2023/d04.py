#!/usr/bin/env python
import sys


if __name__ == '__main__':
    total1 = 0
    total2 = 0
    cards = []
    for line in sys.stdin:
        _, numbers = line.strip().split(': ')
        winners, held = numbers.split(' | ')
        winners = {int(x) for x in winners.split()}
        held = {int(x) for x in held.split()}
        hits = winners & held
        if hits:
            total1 += 2 ** (len(hits) - 1)
        cards.append([1, len(hits)])
    print(total1)

    total2 = 0
    for i, card in enumerate(cards):
        count, hits = card
        total2 += count
        for j in range(i + 1, i + hits + 1):
            cards[j][0] += count
    print(total2)
