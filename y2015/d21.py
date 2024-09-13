import math
from collections import namedtuple
from itertools import product, combinations

from rich import print


Item = namedtuple('item', ['name', 'cost', 'damage', 'armor'])
Character = namedtuple('character', ['health', 'damage', 'armor'])
Equipment = namedtuple('equipment', ['weapon', 'armor', 'ring1', 'ring2'])


WEAPONS = (
        Item('Dagger', 8, 4, 0),
        Item('Shortsword', 10, 5, 0),
        Item('Warhammer', 25, 6, 0),
        Item('Longsword', 40, 7, 0),
        Item('Greataxe', 74, 8, 0),
        )
ARMOR = (
        Item('Leather', 13, 0, 1),
        Item('Chainmail', 31, 0, 2),
        Item('Splintmail', 53, 0, 3),
        Item('Bandedmail', 75, 0, 4),
        Item('Platemail', 102, 0, 5),
        )
RINGS = (
        Item('Damage +1', 25, 1, 0),
        Item('Damage +2', 50, 2, 0),
        Item('Damage +3', 100, 3, 0),
        Item('Defense +1', 20, 0, 1),
        Item('Defense +2', 40, 0, 2),
        Item('Defense +3', 80, 0, 3),
        )


def parse(stream) -> tuple:
    result = []
    for line in stream:
        label, value = line.strip().split(': ')
        result.append(int(value))
    return Character(*result)


def get_equipment_totals(equipment: Equipment) -> tuple:
    """Return the total cost, damage and armor values of a loadout."""
    cost = 0
    damage = 0
    armor = 0
    for item in equipment:
        if item is None:
            continue
        cost += item.cost
        damage += item.damage
        armor += item.armor
    return (cost, damage, armor)


def fight(boss, player, equip_damage, equip_armor) -> tuple:
    """Run a combat scenario.

    The scenario is played out until either the player or the boss runs out of
    health.

    The result is a tuple of [boss health, player health, turn].
    """
    damage = player.damage + equip_damage
    armor = player.armor + equip_armor

    player_dpt = max(1, damage - boss.armor)
    boss_dpt = max(1, boss.damage - armor)

    player_win = math.ceil(boss.health / player_dpt)
    boss_win = math.ceil(player.health / boss_dpt)

    if boss_win < player_win:
        return (
                boss.health - player_dpt * boss_win,
                player.health - boss_dpt * boss_win,
                boss_win * 2)
    else:
        return (
                boss.health - player_dpt * player_win,
                player.health - boss_dpt * (player_win - 1),
                player_win * 2 - 1)


def get_all_loadouts():
    """Return an iterator across all valid equipment loadouts.

    A valid equipment loadout has:
    - exactly one weapon
    - one armor or no armor
    - no ring, one ring, or any combination of two rings
    """
    weapons = WEAPONS
    armor = ARMOR + (None,)
    rings = [(None, None)] + [(x, None) for x in RINGS]
    rings.extend(combinations(RINGS, 2))

    result = []
    for w, a, (r1, r2) in product(weapons, armor, rings):
        e = Equipment(w, a, r1, r2)
        result.append(e)
    return result


def find_cheapest_winning_loadout(boss, player):
    loadouts = [(x, get_equipment_totals(x)) for x in get_all_loadouts()]
    loadouts.sort(key=lambda x: x[1][0])
    for equip, (cost, damage, armor) in loadouts:
        result = fight(boss, player, damage, armor)
        if result[0] <= 0:
            print(f"Player wins with loadout costing {cost}:")
            print(equip)
            return result


def find_costliest_losing_loadout(boss, player):
    loadouts = [(x, get_equipment_totals(x)) for x in get_all_loadouts()]
    loadouts.sort(key=lambda x: x[1][0], reverse=True)
    for equip, (cost, damage, armor) in loadouts:
        result = fight(boss, player, damage, armor)
        if result[1] <= 0:
            print(f"Player loses with loadout costing {cost}:")
            print(equip)
            return result


def run(stream, test=False, draw=False):
    boss = parse(stream)
    if test:
        player = Character(8, 5, 5)
        result1 = fight(boss, player, 0, 0)
        result2 = 0
    else:
        player = Character(100, 0, 0)
        result1 = find_cheapest_winning_loadout(boss, player)
        result2 = find_costliest_losing_loadout(boss, player)

    return (result1, result2)
