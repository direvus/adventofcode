import re
from collections import defaultdict
from itertools import combinations_with_replacement

from rich import print


PATTERN = re.compile(
        r'(\w+): .+ (-?\d+),.+ (-?\d+),.+ (-?\d+),.+ (-?\d+),.+ (-?\d+)')


class Ingredient:
    def __init__(
            self, name: str, capacity: int,
            durability: int, flavour: int, texture: int, calories: int = 0):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavour = flavour
        self.texture = texture
        self.calories = calories


class Recipe:
    def __init__(self):
        self.ingredients = []

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            m = PATTERN.match(line)
            if not m:
                print(f"'{line}' didn't match")
                continue
            name, cap, dur, fla, tex, cal = m.groups()
            cap = int(cap)
            dur = int(dur)
            fla = int(fla)
            tex = int(tex)
            cal = int(cal)
            g = Ingredient(name, cap, dur, fla, tex, cal)
            self.ingredients.append(g)

    def get_score(self, amounts: list[int]) -> int:
        cap = 0
        dur = 0
        fla = 0
        tex = 0
        for i, amount in enumerate(amounts):
            g = self.ingredients[i]
            cap += amount * g.capacity
            dur += amount * g.durability
            fla += amount * g.flavour
            tex += amount * g.texture
        cap = max(0, cap)
        dur = max(0, dur)
        fla = max(0, fla)
        tex = max(0, tex)
        return cap * dur * fla * tex

    def get_total_calories(self, amounts: list[int]) -> int:
        cal = 0
        for i, amount in enumerate(amounts):
            g = self.ingredients[i]
            cal += amount * g.calories
        return cal

    def get_best_score(self, total: int = 100) -> int:
        n = len(self.ingredients)
        bins = defaultdict(lambda: 0)
        best = float('-inf')
        for combo in combinations_with_replacement(range(n), total):
            for i in combo:
                bins[i] += 1
            amounts = [bins[i] for i in range(n)]
            score = self.get_score(amounts)
            if score > best:
                best = score
            bins.clear()
        return best

    def get_best_score_for_calories(self, cal: int, total: int = 100) -> int:
        n = len(self.ingredients)
        bins = defaultdict(lambda: 0)
        best = float('-inf')
        for combo in combinations_with_replacement(range(n), total):
            bins.clear()
            for i in combo:
                bins[i] += 1
            amounts = [bins[i] for i in range(n)]
            if self.get_total_calories(amounts) != cal:
                continue
            score = self.get_score(amounts)
            if score > best:
                best = score
        return best


def run(stream, test=False):
    recipe = Recipe()
    recipe.parse(stream)

    result1 = recipe.get_best_score()
    result2 = recipe.get_best_score_for_calories(500)
    return (result1, result2)
