#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import Counter
from pprint import PrettyPrinter
from typing import List

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"


def read_ages() -> List[int]:
    ages: List[int] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                ages = [int(num) for num in line.split(",")]
    return ages


def simulate_fish(fishes: List[int]) -> int:
    fish_counter = Counter(fishes)
    live_fish_counter = fish_counter.copy()
    born_fish = {}
    for _ in range(0, 256):
        for timer, fish_count in sorted(fish_counter.items()):
            if timer > 0:
                live_fish_counter[timer - 1] = fish_count
                del live_fish_counter[timer]
            if timer == 0:
                born_fish[8] = fish_count
                del live_fish_counter[0]
                born_fish[6] = fish_count
        fish_counter = live_fish_counter.copy()
        fish_counter[8] += born_fish.get(8, 0)
        fish_counter[6] += born_fish.get(6, 0)
        born_fish = {}
    return sum([v for v in fish_counter.values() if v])


def solve() -> int:
    ages = read_ages()
    return simulate_fish(ages)


def main():
    number_of_fish = solve()
    print(f"Result: {number_of_fish}")


if __name__ == "__main__":
    sys.exit(main())
