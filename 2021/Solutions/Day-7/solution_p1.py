#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
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


def read_horizontal_positions() -> List[int]:
    positions: List[int] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                positions = [int(num) for num in line.split(",")]
    return positions


def find_position_with_least_fuel(positions: List[int]) -> int:
    min_fuel = float("inf")
    for position in sorted(positions):
        fuel_amount = 0
        for other_pos in [pos for pos in positions if pos != position]:
            fuel_amount += abs(other_pos - position)
        min_fuel = min(min_fuel, fuel_amount)
    return min_fuel


def solve() -> int:
    positions = read_horizontal_positions()
    return find_position_with_least_fuel(positions)


def main():
    fuel_consumption = solve()
    print(f"Result: {fuel_consumption}")


if __name__ == "__main__":
    sys.exit(main())
