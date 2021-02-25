#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

INPUT_FILE = "input.txt"


def calculate_sum_of_yes_counts():
    yes_count = list()
    counts = set()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                for char in line:
                    counts.add(char)
            if not line and counts:
                yes_count.append(len(counts))
                counts.clear()
    yes_count.append(len(counts))
    print(sum(yes_count))


def main():
    calculate_sum_of_yes_counts()


if __name__ == "__main__":
    sys.exit(main())
