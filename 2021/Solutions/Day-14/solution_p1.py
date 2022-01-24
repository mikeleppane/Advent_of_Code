#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter, defaultdict

import re
import sys
from itertools import pairwise
from pprint import PrettyPrinter
from typing import Dict, List, Tuple, DefaultDict

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"
NUMBER_OF_STEPS = 10


def start_pair_insertion_process(template: List[str], rules: Dict[str, str]) -> int:
    recipe: DefaultDict[str, int] = defaultdict(int)
    polymer_counter = Counter("".join(template))
    for polymer_pair in pairwise(template):
        if "".join(polymer_pair) in recipe:
            recipe["".join(polymer_pair)] += 1
        else:
            recipe["".join(polymer_pair)] = recipe.get("".join(polymer_pair), 1)
    for _ in range(NUMBER_OF_STEPS):
        pairs = {}
        for pair, result in rules.items():
            if pair in recipe and recipe[pair] > 0:
                pairs.update({pair: result})
        new_pairs: DefaultDict[str, int] = defaultdict(int)
        for pair, result in pairs.items():
            polymer_counter[result] += recipe[pair]
            first_pair = pair[0] + result
            second_pair = result + pair[1]
            new_pairs[first_pair] += recipe[pair]
            new_pairs[second_pair] += recipe[pair]
            recipe[pair] = 0
        for pair, value in new_pairs.items():
            recipe[pair] = value

    most_commons = polymer_counter.most_common(len(polymer_counter))
    return most_commons[0][1] - most_commons[-1][1]


def read_polymers() -> Tuple[List[str], Dict[str, str]]:
    template: List[str] = []
    rules: Dict[str, str] = {}
    insertion_regex = re.compile(r"^(\w+)\s+->\s+(\w)")
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for index, line in enumerate(f_handle):
            line = line.rstrip()
            if line:
                if index == 0:
                    template = list(line)
                else:
                    if m := insertion_regex.match(line):
                        rules.update({m.group(1): m.group(2)})

    return template, rules


def solve() -> int:
    template, rules = read_polymers()
    return start_pair_insertion_process(template, rules)


def main():
    result = solve()
    print(f"Result: {result}")


if __name__ == "__main__":
    sys.exit(main())
