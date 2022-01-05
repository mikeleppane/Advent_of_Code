#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from dataclasses import dataclass
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

INPUT_FILE = "test_input.txt"


@dataclass
class LanternFish:
    timer: int


def read_ages() -> List[int]:
    ages: List[int] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                ages = [int(num) for num in line.split(",")]
    return ages


def create_initial_lanternfish(ages: List[int]) -> List[LanternFish]:
    fishes: List[LanternFish] = []
    for age in ages:
        fishes.append(LanternFish(timer=age))
    return fishes


def simulate_fish(fishes: List[LanternFish]) -> int:
    for day in range(0, 80):
        new_fishes: List[LanternFish] = []
        for fish in fishes:
            if fish.timer == 0:
                new_fishes.append(LanternFish(timer=8))
                fish.timer = 6
            else:
                fish.timer -= 1
        for fish in new_fishes:
            fishes.append(fish)
    return len(fishes)


def solve() -> int:
    ages = read_ages()
    initial_fishes = create_initial_lanternfish(ages)
    return simulate_fish(initial_fishes)


def main():
    number_of_fish = solve()
    print(f"Result: {number_of_fish}")


if __name__ == "__main__":
    sys.exit(main())
