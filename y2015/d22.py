"""Advent of Code 2015

Day 22: Wizard Simulator 20XX

https://adventofcode.com/2015/day/22
"""
import logging
import os
from collections import namedtuple

from PIL import Image

import visualise


Player = namedtuple('player', ['health', 'mana'])
Boss = namedtuple('boss', ['health', 'damage'])


SPELLS = {
        'Magic Missile': 53,
        'Drain': 73,
        'Shield': 113,
        'Poison': 173,
        'Recharge': 229,
        }
ASSETDIR = 'assets/wizardsim'


class Game:
    def __init__(
            self,
            boss: Boss = None,
            player: Player = None,
            difficulty: int = 0,
            draw: bool = False):
        self.difficulty = difficulty
        self.turn = 0
        self.effects = []
        self.animation = None
        self.boss_damage = boss.damage if boss else None
        self.boss_hp = boss.health if boss else None
        self.player_hp = player.health if player else None
        self.mana = player.mana if player else None

        if draw:
            background = Image.open('assets/wizardsim/background.png')
            self.animation = visualise.Animation(
                    background.size, 24, background)
            self.player_sprite = PlayerSprite()
            self.animation.add_element(self.player_sprite)

    @property
    def as_tuple(self) -> tuple:
        return (
                self.difficulty,
                self.turn,
                self.boss_hp,
                self.boss_damage,
                self.player_hp,
                self.mana,
                self.effects,
                )

    @classmethod
    def from_tuple(cls, value):
        game = cls()
        (
                game.difficulty,
                game.turn,
                game.boss_hp,
                game.boss_damage,
                game.player_hp,
                game.mana,
                game.effects,
                ) = value
        return game

    def do_effects(self) -> int:
        """Apply all the current spell effects.

        Each effect will be applied to the game state and its timer will be
        reduced. Effects that expire will be removed from the effects list.

        Return the total armor buff resulting from the effects.
        """
        next_effects = []
        armor = 0
        for effect, timer in self.effects:
            match effect:
                case 'Shield':
                    armor += 7
                case 'Poison':
                    self.boss_hp -= 3
                case 'Recharge':
                    self.mana += 101
            timer -= 1
            if timer > 0:
                next_effects.append((effect, timer))
        self.effects = next_effects
        return armor

    def do_round(self, action: str) -> bool | None:
        """Run one round of this game.

        A round is one player turn, followed (possibly) by one enemy turn.

        At the end of the round, return a boolean or None showing the current
        win state (True: player wins, False: enemy wins, None: undecided).
        """
        if self.difficulty > 0:
            # Hard mode - player loses health
            self.player_hp -= 1
            if self.player_hp <= 0:
                return False

        turn_armor = self.do_effects()

        if self.boss_hp <= 0:
            return True

        # Player turn
        if not action:
            logging.debug(
                    f"Player has no action selected on turn {self.turn + 1}")
            return False
        self.mana -= SPELLS[action]
        if self.mana < 0:
            logging.debug(
                    f"Not enough mana to cast {action} "
                    f"on turn {self.turn + 1}")
            return False
        active = {name for name, _ in self.effects}
        if action in active:
            logging.debug(
                    f"Cannot cast {action} on turn {self.turn + 1}, "
                    "it is active")
            return False
        match action:
            case 'Magic Missile':
                self.boss_hp -= 4
            case 'Drain':
                self.boss_hp -= 2
                self.player_hp += 2
            case 'Shield':
                self.effects.append((action, 6))
            case 'Poison':
                self.effects.append((action, 6))
            case 'Recharge':
                self.effects.append((action, 5))

        if self.boss_hp <= 0:
            return True

        self.turn += 1
        turn_armor = self.do_effects()

        if self.boss_hp <= 0:
            return True

        # Enemy turn
        self.player_hp -= max(1, self.boss_damage - turn_armor)

        if self.player_hp <= 0:
            return False
        self.turn += 1
        return None


class PlayerSprite(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'wizard.png')
        position = (72, 102)
        super().__init__(image, position, start=0, fade_in=24)


class BossSprite(visualise.Sprite):
    pass


def parse(stream) -> tuple:
    result = []
    for line in stream:
        label, value = line.strip().split(': ')
        result.append(int(value))
    return Boss(*result)


def fight(boss, player, actions, draw: bool = False) -> tuple:
    """Run a combat scenario.

    The player will cast the spells listed in `actions` in order on their
    turns, and the combat will be played out until either character runs out of
    hit points. If the player doesn't have enough mana to cast the selected
    spell on their turn, or they run out of actions, or they try to cast a
    spell with an effect that is already in play, they lose immediately.

    Return a tuple of (player won, boss health, player health, turn number)
    after the fight ends.
    """
    game = Game(boss, player, draw=draw)
    outcome = None
    for action in actions:
        outcome = game.do_round(action)
        if outcome is not None:
            break

    if draw:
        game.animation.render('out/y2015d22.gif', stop=48)

    return (outcome, game.boss_hp, game.player_hp, game.turn)


def get_total_mana_cost(actions):
    return sum(SPELLS[x] for x in actions)


def find_least_mana_win(boss, player, difficulty: int = 0) -> int:
    """Find the way to win the game while spending the least mana.

    Explore all the possible movesets in a breadth-first way. Return the total
    cost of the cheapest moveset that wins the game.
    """
    init = Game(boss, player, difficulty).as_tuple
    best = float('inf')
    # All spells are possible in the first round
    q = [(init, 0, action) for action in SPELLS.keys()]

    while q:
        state, cost, action = q.pop(0)
        cost += SPELLS[action]
        if cost >= best:
            # This route is a dead-end, even if we win it can't possibly beat
            # the best cost found so far.
            continue
        game = Game.from_tuple(state)
        win = game.do_round(action)
        if win:
            if cost < best:
                best = cost
            continue
        if win is False:
            # Player lost, abandon this route.
            continue

        # This game is still in play. Choose possible next spells from the list
        # of spells that won't be in effect next round, and that the player can
        # afford to cast.
        active = {name for name, timer in game.effects if timer > 1}
        spells = [
                name for name, cost in SPELLS.items()
                if cost <= game.mana and name not in active]
        spells.sort(key=lambda x: SPELLS[x])
        state = game.as_tuple
        for action in spells:
            q.append((state, cost, action))
    return best


def run(stream, test=False, draw=False):
    boss = parse(stream)
    if test:
        player = Player(10, 250)
        actions = ('Recharge', 'Shield', 'Drain', 'Poison', 'Magic Missile')
        result1 = fight(boss, player, actions, draw)
        result2 = find_least_mana_win(boss, Player(10, 500), 1)
    else:
        player = Player(50, 500)
        result1 = find_least_mana_win(boss, player)
        result2 = find_least_mana_win(boss, player, 1)

    return (result1, result2)
