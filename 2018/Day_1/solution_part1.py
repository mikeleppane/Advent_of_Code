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


def calculate_total_frequency(frequencies: List[int]):
    print(f"Total frequency is: {sum(frequencies)}")


def main():
    frequencies = read_frequencies()
    calculate_total_frequency(frequencies)


if __name__ == "__main__":
    sys.exit(main())
