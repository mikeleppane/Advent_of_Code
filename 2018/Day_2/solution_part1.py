#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List
from itertools import groupby
from collections import Counter
from math import prod

INPUT_FILE = "input.txt"


def read_box_ids() -> List[str]:
    inputs = []
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            inputs.append(line.strip())
    return inputs


def calculate_checksum(ids: List[str]):
    letter_counter = Counter()
    letter_counter[2] = 0
    letter_counter[3] = 0
    for id in ids:
        counts = set()
        for _, g in groupby("".join(sorted(id))):
            count = len(list(g))
            if count not in counts:
                letter_counter[count] += 1
                counts.add(count)

    print(prod((letter_counter[2], letter_counter[3])))


def main():
    box_ids = read_box_ids()
    calculate_checksum(box_ids)


if __name__ == "__main__":
    sys.exit(main())
