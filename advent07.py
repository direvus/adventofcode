#!/usr/bin/env python
import sys


TRANS = str.maketrans('23456789TJQKA', 'abcdefghijklm')


def get_hand_type(hand: str) -> int:
    """Return the type of hand, given a 5-character hand string.

    The returned value is an integer ranging from 0-6 as follows:

    - 6 = Five of a kind
    - 5 = Four of a kind
    - 4 = Full house
    - 3 = Three of a kind
    - 2 = Two pair
    - 1 = One pair
    - 0 = Nothing
    """
    s = set(hand)
    match len(s):
        case 1:
            # Five of a kind
            return 6
        case 2:
            # Either a full house or a four-of-a-kind
            count = hand.count(hand[0])
            return 5 if count in {1, 4} else 4
        case 3:
            # Either a three-of-a-kind or a two pair
            counts = {hand.count(x) for x in s}
            return 3 if 3 in counts else 2
        case 4:
            # One pair
            return 1
        case 5:
            # No pair
            return 0


def get_hand_key(hand: str) -> str:
    """Return a sort key for a hand.

    This key can be passed to a sort method to yield a correct sort
    order from weakest to strongest, across any collection of hands.
    """
    return str(get_hand_type(hand)) + hand.translate(TRANS)


if __name__ == '__main__':
    hands = []
    for line in sys.stdin:
        hand, bid = line.strip().split()
        hands.append((hand, int(bid)))
    hands.sort(key=lambda x: get_hand_key(x[0]))

    total1 = 0
    i = 1
    for hand, bid in hands:
        total1 += i * bid
        i += 1
    print(total1)
