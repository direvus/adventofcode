"""Advent of Code 2015

Day 22: Wizard Simulator 20XX

https://adventofcode.com/2015/day/22
"""
import logging
import os
from collections import namedtuple
from operator import add, sub

from PIL import Image, ImageFont

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

# Visualisation settings
ASSETDIR = 'assets/wizardsim'
FRAMERATE = 24
BEAT = 12
LONG_BEAT = 24
PLAYER_POSITION = (72, 102)
BOSS_POSITION = (384, 102)

# Pixel12x10 is by Corne2Plum3, and the repo is located at
# https://github.com/Corne2Plum3/Pixel12x10
FONTPATH = os.path.join(ASSETDIR, 'Pixel12x10-v1.1.0.ttf')
FONT = ImageFont.truetype(FONTPATH, 72)


class Game:
    def __init__(
            self,
            boss: Boss = None,
            player: Player = None,
            difficulty: int = 0,
            draw: bool = False):
        self.difficulty = difficulty
        self.turn = 0
        self.time = 0
        self.actions = []
        self.effects = []
        self.animation = None

        if boss:
            self.boss_damage = boss.damage
            self.boss_hp = boss.health
            self.boss_max_hp = boss.health
        else:
            self.boss_damage = None
            self.boss_hp = None
            self.boss_max_hp = None

        if player:
            self.player_hp = player.health
            self.player_max_hp = player.health
            self.player_mana = player.mana
            self.player_max_mana = player.mana
        else:
            self.player_hp = None
            self.player_max_hp = None
            self.player_mana = None
            self.player_max_mana = None

        if draw:
            background = Image.open('assets/wizardsim/background.png')
            self.animation = visualise.Animation(
                    background.size, FRAMERATE, background)
            self.player_sprite = PlayerSprite()
            self.boss_sprite = BossSprite()
            self.player_health_bar = PlayerHealthBar()
            self.boss_health_bar = BossHealthBar()
            self.player_mana_bar = PlayerManaBar()

            self.animation.add_elements(
                    self.player_sprite,
                    self.boss_sprite,
                    self.player_health_bar,
                    self.boss_health_bar,
                    self.player_mana_bar,
                    )
            self.shield_sprite = None

    @property
    def as_tuple(self) -> tuple:
        return (
                self.difficulty,
                self.turn,
                self.boss_hp,
                self.boss_max_hp,
                self.boss_damage,
                self.player_hp,
                self.player_max_hp,
                self.player_mana,
                self.player_max_mana,
                tuple(self.actions),
                tuple(self.effects),
                )

    @classmethod
    def from_tuple(cls, value):
        game = cls()
        (
                game.difficulty,
                game.turn,
                game.boss_hp,
                game.boss_max_hp,
                game.boss_damage,
                game.player_hp,
                game.player_max_hp,
                game.player_mana,
                game.player_max_mana,
                actions,
                effects,
                ) = value
        game.actions = list(actions)
        game.effects = list(effects)
        return game

    def add_message(self, message: str):
        if not self.animation:
            return
        element = MessageBox(
                text=message,
                start=self.time,
                stop=self.time + LONG_BEAT * 2,
                fade_in=BEAT,
                fade_out=BEAT)
        self.animation.add_element(element)

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
                    self.add_message(f'{effect}:\n3 DMG')
                    self.modify_boss_hp(-3)
                    self.do_boss_knockback()
                    self.time += LONG_BEAT * 2
                case 'Recharge':
                    self.add_message(f'{effect}:\n+101 MP')
                    self.modify_player_mana(101)
                    self.time += LONG_BEAT * 2
            timer -= 1
            if timer > 0:
                next_effects.append((effect, timer))
            else:
                self.do_end_effect(effect)
        self.effects = next_effects
        return armor

    def do_end_effect(self, effect):
        if not self.animation:
            return

        self.add_message(f'{effect}\nends.')
        match effect:
            case 'Shield':
                self.shield_sprite.stop = self.time
                self.shield_sprite.fade_out = BEAT
            case 'Recharge':
                self.recharge_sprite.stop = self.time
                self.recharge_sprite.fade_out = BEAT
            case 'Poison':
                self.poison_sprite.stop = self.time
                self.poison_sprite.fade_out = BEAT
        self.time += LONG_BEAT * 2

    def modify_player_hp(self, diff: int) -> int:
        prev = self.player_hp
        self.player_hp += diff
        if self.animation and diff != 0:
            maxhp = self.player_max_hp
            bar = self.player_health_bar
            width, height = bar.image.size
            p = prev / maxhp
            p = max(0, min(1, p))
            initial = (0, 0, round(width * p), height)
            p = self.player_hp / maxhp
            p = max(0, min(1, p))
            final = (0, 0, round(width * p), height)
            bar.add_crop(self.time, BEAT, initial, final)
        return self.player_hp

    def modify_boss_hp(self, diff: int) -> int:
        prev = self.boss_hp
        self.boss_hp += diff
        if self.animation and diff != 0:
            bar = self.boss_health_bar
            maxhp = self.boss_max_hp
            width, height = bar.image.size
            p = (maxhp - prev) / maxhp
            p = max(0, min(1, p))
            initial = (round(width * p), 0, width, height)
            p = (maxhp - self.boss_hp) / maxhp
            p = max(0, min(1, p))
            final = (round(width * p), 0, width, height)
            bar.add_crop(self.time, BEAT, initial, final)
        return self.boss_hp

    def modify_player_mana(self, diff: int) -> int:
        prev = self.player_mana
        self.player_mana += diff
        if self.animation and diff != 0:
            maxmana = self.player_max_mana
            bar = self.player_mana_bar
            width, height = bar.image.size
            p = prev / maxmana
            p = max(0, min(1, p))
            initial = (0, 0, round(width * p), height)
            p = self.player_mana / maxmana
            p = max(0, min(1, p))
            final = (0, 0, round(width * p), height)
            bar.add_crop(self.time, BEAT, initial, final)
        return self.player_mana

    def do_player_win(self):
        if not self.animation:
            return

        interval = BEAT // 2
        sprite = self.boss_sprite
        for _ in range(2):
            sprite.add_fade(self.time, interval, 1.0, 0.0)
            self.time += interval
            sprite.add_fade(self.time, interval, 0.0, 1.0)
            self.time += interval

        self.boss_health_bar.stop = self.time
        self.boss_health_bar.fade_out = LONG_BEAT
        sprite.stop = self.time
        sprite.fade_out = LONG_BEAT

        self.add_message('BOSS\nDEFEATED!')

    def do_player_loss(self):
        if not self.animation:
            return

        self.time += LONG_BEAT
        self.player_health_bar.stop = self.time
        self.player_health_bar.fade_out = LONG_BEAT
        self.player_sprite.stop = self.time
        self.player_sprite.fade_out = LONG_BEAT
        self.add_message('GAME\nOVER!')

    def do_player_knockback(self):
        if not self.animation:
            return

        sprite = self.player_sprite
        position = PLAYER_POSITION
        vector = (-12, 0)
        reverse = (12, 0)
        dest = tuple(map(add, position, vector))

        sprite.add_movement(self.time, BEAT, position, vector)
        sprite.add_movement(self.time + BEAT, BEAT, dest, reverse)

    def do_boss_attack(self):
        if not self.animation:
            return

        sprite = self.boss_sprite
        position = BOSS_POSITION
        x, y = position
        vector = (132 - x, 0)
        reverse = (x - 132, 0)
        dest = tuple(map(add, position, vector))

        sprite.add_movement(
                self.time, BEAT, position, vector,
                easing=visualise.ease_cubic_in)
        sprite.add_movement(self.time + BEAT, BEAT, dest, reverse)

    def do_boss_knockback(self):
        if not self.animation:
            return

        sprite = self.boss_sprite
        position = BOSS_POSITION
        vector = (12, 0)
        reverse = (-12, 0)
        dest = tuple(map(add, position, vector))

        sprite.add_movement(self.time, BEAT, position, vector)
        sprite.add_movement(self.time + BEAT, BEAT, dest, reverse)

    def do_recharge(self):
        self.effects.append(('Recharge', 5))
        if not self.animation:
            return

        self.add_message('Recharge\nbegins!')
        path = os.path.join(ASSETDIR, 'recharge.png')
        image = Image.open(path)
        width, _ = image.size
        position = (0, 72)

        sprite = visualise.Sprite(
                image, position, start=self.time, fade_in=BEAT)
        self.recharge_sprite = sprite
        self.animation.add_element(sprite)

    def do_poison(self):
        self.effects.append(('Poison', 6))
        if not self.animation:
            return

        self.add_message('Poison\nbegins!')
        path = os.path.join(ASSETDIR, 'poison.png')
        image = Image.open(path)
        width, _ = image.size
        position = (444, 72)

        sprite = visualise.Sprite(
                image, position, start=self.time, fade_in=BEAT)
        self.poison_sprite = sprite
        self.animation.add_element(sprite)

    def do_shield(self):
        self.effects.append(('Shield', 6))
        if not self.animation:
            return

        self.add_message('Shield\nbegins!')
        path = os.path.join(ASSETDIR, 'shield.png')
        image = Image.open(path)
        width, _ = image.size
        crop = (0, 0, width, 132)
        image = image.crop(crop)
        position = (18, 72)

        shield = visualise.Sprite(
                image, position, start=self.time, fade_in=BEAT)
        self.shield_sprite = shield
        self.animation.add_element(shield)

    def do_magic_missile(self):
        if not self.animation:
            self.modify_boss_hp(-4)
            return

        self.add_message('Magic Msl:\n4 DMG')
        path = os.path.join(ASSETDIR, 'missile.png')
        image = Image.open(path)
        position = (138, 156)
        vector = (396 - position[0], 0)

        sprite = visualise.Sprite(
                image, position, start=self.time,
                stop=(self.time + LONG_BEAT), fade_in=(BEAT // 2))
        sprite.add_movement(
                self.time, LONG_BEAT, position, vector,
                easing=visualise.ease_exp_in)
        self.animation.add_element(sprite)

        self.time += LONG_BEAT
        self.do_boss_knockback()
        self.modify_boss_hp(-4)

    def do_drain(self):
        damage = 2
        if not self.animation:
            self.modify_boss_hp(-damage)
            self.modify_player_hp(damage)
            return

        self.add_message(f'Drain:\n{damage} DMG > +HP')

        path = os.path.join(ASSETDIR, 'drain.png')
        image = Image.open(path)
        origin = (396, 120)
        dest = (126, 156)
        vector = tuple(map(sub, dest, origin))

        sprite = visualise.Sprite(
                image, origin, start=self.time,
                stop=(self.time + LONG_BEAT), fade_in=(BEAT // 2))
        sprite.add_movement(
                self.time, LONG_BEAT, origin, vector)
        self.animation.add_element(sprite)

        self.do_boss_knockback()
        self.time += LONG_BEAT
        self.modify_boss_hp(-2)
        self.modify_player_hp(2)

    def do_action(self, action):
        match action:
            case 'Magic Missile':
                self.do_magic_missile()
            case 'Drain':
                self.do_drain()
            case 'Shield':
                self.do_shield()
            case 'Poison':
                self.do_poison()
            case 'Recharge':
                self.do_recharge()

    def do_round(self, action: str) -> bool | None:
        """Run one round of this game.

        A round is one player turn, followed (possibly) by one enemy turn.

        At the end of the round, return a boolean or None showing the current
        win state (True: player wins, False: enemy wins, None: undecided).
        """
        self.time += BEAT

        if self.difficulty > 0:
            self.add_message('Hard mode:\n-1 HP')
            self.modify_player_hp(-1)
            self.time += LONG_BEAT * 2
            if self.player_hp <= 0:
                return False

        turn_armor = self.do_effects()

        if self.boss_hp <= 0:
            self.do_player_win()
            return True

        # Player turn
        if not action:
            logging.debug(
                    f"Player has no action selected on turn {self.turn + 1}")
            self.do_player_loss()
            return False

        self.actions.append(action)
        self.modify_player_mana(-SPELLS[action])

        if self.player_mana < 0:
            logging.debug(
                    f"Not enough mana to cast {action} "
                    f"on turn {self.turn + 1}")
            self.do_player_loss()
            return False
        active = {name for name, _ in self.effects}
        if action in active:
            logging.debug(
                    f"Cannot cast {action} on turn {self.turn + 1}, "
                    "it is active")
            self.do_player_loss()
            return False

        self.do_action(action)

        if self.boss_hp <= 0:
            self.do_player_win()
            return True

        self.turn += 1
        self.time += LONG_BEAT * 2
        turn_armor = self.do_effects()

        if self.boss_hp <= 0:
            self.do_player_win()
            return True

        # Enemy turn
        damage = max(1, self.boss_damage - turn_armor)
        self.modify_player_hp(-damage)
        self.add_message(f'Boss atk:\n-{damage} HP')
        self.do_boss_attack()
        self.time += BEAT
        self.do_player_knockback()
        self.time += BEAT

        if self.player_hp <= 0:
            self.do_player_loss()
            return False
        self.turn += 1
        self.time += LONG_BEAT
        return None


class PlayerSprite(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'wizard.png')
        position = PLAYER_POSITION
        super().__init__(image, position, start=0, fade_in=LONG_BEAT)


class BossSprite(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'boss.png')
        position = BOSS_POSITION
        x, y = position
        origin = (x + 180, y)  # Start off-screen
        vector = (-180, 0)
        super().__init__(image, origin, start=LONG_BEAT)
        self.add_movement(LONG_BEAT, LONG_BEAT, origin, vector)


class PlayerHealthBar(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'healthbar.png')
        position = (12, 12)
        super().__init__(image, position, start=0, fade_in=LONG_BEAT)


class BossHealthBar(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'healthbar.png')
        position = (312, 12)
        super().__init__(image, position, start=0, fade_in=LONG_BEAT)


class PlayerManaBar(visualise.Sprite):
    def __init__(self):
        image = os.path.join(ASSETDIR, 'manabar.png')
        position = (12, 42)
        super().__init__(image, position, start=0, fade_in=LONG_BEAT)


class MessageBox(visualise.Text):
    def __init__(self, *args, **kwargs):
        position = (36, 240)
        size = (502, 160)
        super().__init__(
                FONT, size, position=position, align='left',
                spacing=24, *args, **kwargs)


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
    game.time = LONG_BEAT * 2
    outcome = None
    for action in actions:
        outcome = game.do_round(action)
        if outcome is not None:
            break

    if draw:
        time = game.time + BEAT
        game.animation.render('out/y2015d22.gif', stop=time)

    return (outcome, game.boss_hp, game.player_hp, game.turn)


def get_total_mana_cost(actions):
    return sum(SPELLS[x] for x in actions)


def find_least_mana_win(boss, player, difficulty: int = 0) -> int:
    """Find the way to win the game while spending the least mana.

    Explore all the possible movesets in a breadth-first way. Return the
    cheapest moveset that wins the game and its total mana cost.
    """
    init = Game(boss, player, difficulty).as_tuple
    best = float('inf')
    moves = None
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
                moves = game.actions
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
                if cost <= game.player_mana and name not in active]
        spells.sort(key=lambda x: SPELLS[x])
        state = game.as_tuple
        for action in spells:
            q.append((state, cost, action))
    return moves, best


def run(stream, test=False, draw=False):
    boss = parse(stream)
    if test:
        player = Player(10, 250)
        actions = ('Recharge', 'Shield', 'Drain', 'Poison', 'Magic Missile')
        result1 = fight(boss, player, actions, draw)
        _, result2 = find_least_mana_win(boss, Player(10, 500), 1)
    else:
        player = Player(50, 500)
        moves, result1 = find_least_mana_win(boss, player)
        if draw:
            fight(boss, player, moves, True)

        _, result2 = find_least_mana_win(boss, player, 1)

    return (result1, result2)
