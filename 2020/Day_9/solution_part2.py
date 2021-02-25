#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque

import sys
from itertools import combinations
from typing import List, Deque, Optional

INPUT_FILE = "input.txt"


def find_incorrect_number(numbers: List[int], preamble_size=25) -> Optional[int]:
    preamble: Deque[int] = deque(numbers[:preamble_size])
    next_numbers = numbers[preamble_size:]
    for number in next_numbers:
        if not find_sum_of_numbers(preamble, number):
            return number
        preamble.popleft()
        preamble.append(number)
    return None


def find_sum_of_numbers(preamble: Deque[int], sum_to_be_matched: int) -> bool:
    for values in set(list(combinations(preamble, 2))):
        if sum(values) == sum_to_be_matched:
            print("Found matching numbers")
            return True
    print(f"Cannot find matching pairs for sum of two for number: {sum_to_be_matched}")
    return False


def find_contiguous_set_of_number_to_match_given_number(
    numbers, matched_number
) -> Deque[int]:
    numbers = deque(numbers)
    cache: Deque[int] = deque()
    while True:
        cache.append(numbers.popleft())
        for number in numbers:
            cache.append(number)
            if sum(cache) == matched_number:
                print("Found correct numbers")
                return cache
        cache.clear()
        if not numbers:
            break
    print("Cannot found matching numbers")
    return deque()


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
    number = find_incorrect_number(numbers, preamble_size=25)
    if number:
        set_of_numbers = find_contiguous_set_of_number_to_match_given_number(
            numbers, number
        )
        if set_of_numbers:
            print(
                f"Sum of min and max: {sum(list(sorted(set_of_numbers))[::len(set_of_numbers) - 1])}"
            )
        else:
            print("Did not found any set of matching numbers!")


if __name__ == "__main__":
    sys.exit(main())
