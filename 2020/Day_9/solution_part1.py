#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

import sys
from itertools import combinations
from typing import List, Deque

INPUT_FILE = "input.txt"


def find_incorrect_numbers(numbers: List[int], preamble_size=25):
    preamble: Deque[int] = deque(numbers[:preamble_size])
    next_numbers = numbers[preamble_size:]
    for number in next_numbers:
        find_sum_of_numbers(preamble, number)
        preamble.popleft()
        preamble.append(number)


def find_sum_of_numbers(preamble: Deque[int], sum_to_be_matched: int) -> None:
    for values in set(list(combinations(preamble, 2))):
        if sum(values) == sum_to_be_matched:
            print("Found matching numbers")
            return
    print(f"Cannot find matching pairs for sum of two for number: {sum_to_be_matched}")
    raise ValueError("")


def read_numbers() -> List[int]:
    numbers = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                try:
                    numbers.append(int(line.rstrip()))
                except ValueError as ex:
                    print(f"Cannot convert input value {line.rstrip()} to a int type")
                    raise ValueError from ex
    return numbers


def main():
    numbers = read_numbers()
    find_incorrect_numbers(numbers, preamble_size=25)


if __name__ == "__main__":
    sys.exit(main())
