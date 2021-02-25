#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List

INPUT_FILE = "input.txt"


def read_frequencies() -> List[int]:
    inputs = []
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            inputs.append(int(line.strip()))
    return inputs


def find_first_duplicate_frequency(frequencies: List[int]):
    current_frequency_delta = None
    deltas = set()
    while True:
        for x in frequencies:
            if current_frequency_delta is None:
                current_frequency_delta = x
                deltas.add(current_frequency_delta)
            else:
                current_frequency_delta += x
                if current_frequency_delta in deltas:
                    print(f"Found matching frequency: {current_frequency_delta}")
                    return
                else:
                    deltas.add(current_frequency_delta)


def main():
    frequencies = read_frequencies()
    find_first_duplicate_frequency(frequencies)


if __name__ == "__main__":
    sys.exit(main())
