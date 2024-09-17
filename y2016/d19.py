import logging  # noqa: F401


# Index of the winning player for several small sizes in Part 2.
WINNERS2 = {
        5: 1,
        4: 0,
        3: 2,
        2: 0,
        1: 0,
        }


def parse(stream) -> int:
    return int(stream.readline().strip())


def get_winner(size: int) -> int:
    """Get the last remaining player under Part 1 rules.

    There are `size` players, numbered from one, arranged in a circle.  Each
    player eliminates the next, and play proceeds to the next remaining player,
    until there is only one player left.

    The way this works out with an odd number of players is, all even-numbered
    players are eliminated, and then the last player eliminates the first.

    With an even number of players, only all the even-numbered players are
    eliminated.

    Return the player number of the final player.
    """
    players = [x for x in range(1, size + 1)]
    while size > 1:
        start = 2 if size % 2 else 0
        players = [players[i] for i in range(start, size, 2)]
        size = len(players)
    return players[0]


def get_winner_p2(size: int) -> int:
    """Get the last remaining player under Part 2 rules.

    The rules are similar to Part 1, except that each player eliminates the
    player directly across the circle from them, rounding down in case of a
    tie.

    This ends up eliminating players in a repeating pattern of threes, where we
    eliminate two players in a row and then skip over the third.

    Return the player number of the final player.
    """
    players = tuple(range(1, size + 1))
    while size > 5:
        mod3 = size % 3
        if mod3 == 0:
            # Easy, just retain every third player.
            players = tuple(players[i] for i in range(2, size, 3))
        else:
            # There's probably a more elegant way to form this up, but I got
            # tired of trying to work it out.
            half = size // 2
            start = 1 if size % 2 else 2
            indexes = {(half + i) % size for i in range(start, size, 3)}
            indexes.add(half - 1)
            players = tuple(players[i] for i in sorted(indexes))

        size = len(players)
        logging.debug(f"Reduced to {size} players")
        if size < 20:
            logging.debug(players)
    return players[WINNERS2[size]]


def run(stream, test: bool = False):
    size = parse(stream)

    result1 = get_winner(size)
    result2 = get_winner_p2(size)

    return (result1, result2)
