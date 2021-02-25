#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque, Counter

import sys
from typing import List, Deque

INPUT_FILE = "input.txt"


def find_chain_of_adapter_joins(adapter_ratings: List[int]) -> Counter[str, int]:
    joltage_differences = Counter()
    ratings: Deque[int] = deque(sorted(adapter_ratings))
    ratings.appendleft(0)
    ratings.append(max(ratings) + 3)
    while True:
        prev_adapter_value = ratings.popleft()
        for value in ratings:
            diff = abs(value - prev_adapter_value)
            if diff <= 3:
                joltage_differences[str(diff)] += 1
                print("Found adapter with correct difference")
                break
        if not ratings:
            break
    return joltage_differences


def read_adapter_ratings() -> List[int]:
    adapter_ratings = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                try:
                    adapter_ratings.append(int(line.rstrip()))
                except ValueError as ex:
                    print(f"Cannot convert input value {line.rstrip()} to a int type")
                    raise ValueError from ex
    return adapter_ratings


def main():
    adapter_ratings = read_adapter_ratings()
    differences = find_chain_of_adapter_joins(adapter_ratings)
    print(
        f"Result of 1-jolt times 3 jolts differences: {differences['1'] * differences['3']}"
    )


if __name__ == "__main__":
    sys.exit(main())
