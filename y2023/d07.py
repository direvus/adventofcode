#!/usr/bin/env python
STD = str.maketrans('23456789TJQKA', 'abcdefghijklm')
WILD = str.maketrans('J23456789TQKA', 'abcdefghijklm')


def get_card_counts(hand: str) -> list:
    """Return a list of counts for each card.

    Returns a list of tuples containing the count and card for each
    card present in the hand. For example, a hand of KKTT2 would give
    the result:

        [(2, 'K'), (2, 'T'), (1, '2')]

    Results are ordered from the highest to the lowest card count. If
    multiple cards share the same count then they are returned in no
    specific order.
    """
    cards = set(hand)
    counts = [(hand.count(x), x) for x in cards]
    counts.sort(key=lambda x: x[0], reverse=True)
    return counts


def get_hand_type(hand: str, wilds: bool = False) -> int:
    """Return the type of hand, given a 5-character hand string.

    If `wilds` is true then we use the alternative rules where the J
    card is allowed to act as a wildcard.

    The returned value is an integer ranging from 0-6 as follows:

    - 6 = Five of a kind
    - 5 = Four of a kind
    - 4 = Full house
    - 3 = Three of a kind
    - 2 = Two pair
    - 1 = One pair
    - 0 = Nothing
    """
    counts = get_card_counts(hand)
    if wilds and 'J' in hand:
        # Replace all wilds with whichever card has the highest count.
        #
        # If two cards tie for highest count, it doesn't matter which
        # one we choose so don't worry about it.
        sub = [card for count, card in counts if card != 'J']
        if sub:
            hand = hand.replace('J', sub[0])
        counts = get_card_counts(hand)

    match len(counts):
        case 1:
            # Five of a kind
            return 6
        case 2:
            # Either a full house or a four-of-a-kind
            return 5 if counts[0][0] == 4 else 4
        case 3:
            # Either a three-of-a-kind or a two pair
            return 3 if counts[0][0] == 3 else 2
        case 4:
            # One pair
            return 1
        case 5:
            # No pair
            return 0


def get_hand_key(hand: str, wilds: bool = False) -> str:
    """Return a sort key for a hand.

    If `wilds` is true then we use the alternative rules where the J
    card is considered the weakest for tie breaking purposes.

    This key can be passed to a sort method to yield a correct sort
    order from weakest to strongest, across any collection of hands.
    """
    table = WILD if wilds else STD
    typ = get_hand_type(hand, wilds)
    return str(typ) + hand.translate(table)


def run(stream, test=False):
    hands = []
    for line in stream:
        hand, bid = line.strip().split()
        hands.append((hand, int(bid)))
    hands.sort(key=lambda x: get_hand_key(x[0]))

    total1 = 0
    i = 1
    for hand, bid in hands:
        total1 += i * bid
        i += 1

    hands.sort(key=lambda x: get_hand_key(x[0], True))
    total2 = 0
    i = 1
    for hand, bid in hands:
        total2 += i * bid
        i += 1
    return (total1, total2)
