#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import prod
import sys
from itertools import combinations, product
from typing import Optional, List

INPUT_FILE = "input.txt"


def get_inputs() -> List[int]:
    inputs = []
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            inputs.append(int(line.strip()))
    return inputs


def find_two_entries_with_sum(inputs: List[int], find_sum) -> List[Optional[int]]:
    for values in list(combinations(inputs, 3)):
        if sum(values) == find_sum:
            return list(values)
    return []


def main():
    inputs = get_inputs()
    find_sum = 2020
    values = find_two_entries_with_sum(inputs, find_sum)
    if values:
        print(prod(values))
    else:
        print(f"Could not find any two values that sum to {find_sum}")


if __name__ == "__main__":
    sys.exit(main())
