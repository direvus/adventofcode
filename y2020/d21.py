"""Advent of Code 2020

Day 21: Allergen Assessment

https://adventofcode.com/2020/day/21
"""
import logging  # noqa: F401

from util import timing


class Food:
    def __init__(self, line: str = ''):
        self.ingredients = set()
        self.allergens = set()
        if line:
            self.parse(line)

    def parse(self, line: str):
        assert line.endswith(')')
        left, right = line[:-1].split(' (contains ')
        self.ingredients = set(left.split())
        self.allergens = set(right.split(', '))


class Foods:
    def __init__(self, stream):
        self.foods = []
        self.allergens = set()
        self.ingredients = set()
        self.known = {}
        self.parse(stream)

    def parse(self, stream):
        for line in stream:
            line = line.strip()
            food = Food(line)
            self.foods.append(food)
            self.allergens |= food.allergens
            self.ingredients |= food.ingredients

    def get_ingredients_for_allergen(self, allergen: str) -> set:
        """Return the set of ingredients that possibly contain `allergen`."""
        result = set()
        for food in self.foods:
            if allergen not in food.allergens:
                continue
            if result:
                result &= food.ingredients
            else:
                result = set(food.ingredients)
        exclude = {v for k, v in self.known.items() if k != allergen}
        return result - exclude

    def analyse(self):
        """Attempt to determine which allergens are in which ingredients.

        Continue processing until we have learned everything we can from the
        information at hand. Afterwards, the dictionary in `self.known` will be
        populated with a mapping of allergens to ingredients.
        """
        changes = True
        while changes:
            unknown = self.allergens - set(self.known.keys())
            changes = False
            for allergen in unknown:
                ingreds = self.get_ingredients_for_allergen(allergen)
                if len(ingreds) == 1:
                    ingred = next(iter(ingreds))
                    logging.debug(f"{allergen} must be in {ingred}!")
                    self.known[allergen] = ingred
                    changes = True

    def get_non_allergen_ingredients(self) -> set:
        """Return ingredients that are not known to contain any allergen."""
        return self.ingredients - set(self.known.values())

    def count_ingredients(self, ingredients: set) -> int:
        """Return how many times these ingredients appear in foods."""
        result = 0
        for food in self.foods:
            result += len(food.ingredients & ingredients)
        return result


def parse(stream) -> Foods:
    result = Foods(stream)
    return result


def run(stream, test: bool = False):
    with timing("Part 1"):
        foods = parse(stream)
        foods.analyse()
        ingreds = foods.get_non_allergen_ingredients()
        result1 = foods.count_ingredients(ingreds)

    with timing("Part 2"):
        ingreds = list(foods.known.items())
        ingreds.sort()
        result2 = ','.join(i for a, i in ingreds)

    return (result1, result2)
