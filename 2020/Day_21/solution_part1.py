#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import combinations, islice, permutations
from typing import List, NamedTuple

INPUT_FILE = "input.txt"


class Food(NamedTuple):
    ingredients: List[str]
    allergens: List[str]


def get_unique_ingredients_and_allergens(foods: List[Food]):
    ingredients = set()
    allergens = set()

    for food in foods:
        for ingredient in food.ingredients:
            ingredients.add(ingredient)
        for allergen in food.allergens:
            allergens.add(allergen)

    return ingredients, allergens


def find_ingredient_that_does_not_contain_any_allergens(foods: List[Food]):
    all_ingredients, all_allergens = get_unique_ingredients_and_allergens(foods)
    all_allergens = list(sorted(all_allergens))
    t = {}
    valid = True
    lookup_values = set()
    for values in combinations(all_ingredients, len(all_allergens)):
        is_valid_values = True
        for food in foods:
            u = 0
            for ingredient in food.ingredients:
                if ingredient in values:
                    u += 1
            if u < len(food.allergens):
                is_valid_values = False
                break
        if not is_valid_values:
            continue
        values_sorted = tuple(sorted(values))
        if values_sorted not in lookup_values:
            lookup_values.add(values_sorted)
        else:
            continue
        for vv in permutations(values, len(values)):
            valid = True
            t.clear()
            for i, k in zip(all_allergens, vv):
                t.update({i: k})
            for food in foods:
                for allergen in food.allergens:
                    if not (allergen in t and t[allergen] in food.ingredients):
                        valid = False
                if not valid:
                    break
            if valid:
                break
        if valid:
            break

    if not valid:
        print("Not found any solutions!")
    else:
        print(all_ingredients.difference(set(t.values())))


def read_foods() -> List[Food]:
    foods = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip().rstrip(")")
            if line:
                ingredients, allergens = line.split("(contains")
                ingredients = ingredients.strip().split(" ")
                allergens = [allergen.strip() for allergen in allergens.split(",")]
                foods.append(Food(ingredients=ingredients, allergens=allergens))
    return foods


def main():
    foods = read_foods()
    find_ingredient_that_does_not_contain_any_allergens(foods)


if __name__ == "__main__":
    sys.exit(main())
