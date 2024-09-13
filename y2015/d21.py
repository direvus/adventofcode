from collections import namedtuple
from rich import print


Item = namedtuple('item', ['name', 'cost', 'damage', 'armor'])
Character = namedtuple('character', ['health', 'damage', 'armor'])
Equipment = namedtuple('equipment', ['weapon', 'armor', 'ring1', 'ring2'])


WEAPONS = (
        ('Dagger', 8, 4, 0),
        ('Shortsword', 10, 5, 0),
        ('Warhammer', 25, 6, 0),
        ('Longsword', 40, 7, 0),
        ('Greataxe', 74, 8, 0),
        )
ARMOR = (
        ('Leather', 13, 0, 1),
        ('Chainmail', 31, 0, 2),
        ('Splintmail', 53, 0, 3),
        ('Bandedmail', 75, 0, 4),
        ('Platemail', 102, 0, 5),
        )
RINGS = (
        ('Damage +1', 25, 1, 0),
        ('Damage +2', 50, 2, 0),
        ('Damage +3', 100, 3, 0),
        ('Defense +1', 20, 0, 1),
        ('Defense +2', 20, 0, 2),
        ('Defense +3', 20, 0, 3),
        )


def parse(stream) -> tuple:
    result = []
    for line in stream:
        label, value = line.strip().split(': ')
        result.append(int(value))
    return Character(*result)


def fight(boss, player, equipment) -> tuple:
    """Run a combat scenario.

    The scenario is played out until either the player or the boss runs out of
    health.

    The result is a tuple of [boss health, player health, turn].
    """
    boss_health = boss.health
    player_health = player.health

    damage = player.damage
    armor = player.armor
    for item in equipment:
        if item is None:
            continue
        damage += item.damage
        armor += item.armor

    turn = 0
    while player_health > 0 and boss_health > 0:
        if turn % 2 == 0:
            hits = max(1, damage - boss.armor)
            boss_health -= hits
        else:
            hits = max(1, boss.damage - armor)
            player_health -= hits
        turn += 1
    return (boss_health, player_health, turn)


def run(stream, test=False, draw=False):
    boss = parse(stream)
    equip = Equipment(None, None, None, None)
    if test:
        player = Character(8, 5, 5)
    else:
        player = Character(100, 0, 0)

    print(player)
    print(boss)

    result1 = fight(boss, player, equip)
    result2 = 0
    return (result1, result2)
