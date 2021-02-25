#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import List
from operator import sub
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


def find_common_letters(ids: List[str]):
    for box_id in ids:
        for other_box_id in ids:
            if other_box_id != box_id:
                common = list(map(sub, list(map(ord, tuple(box_id))), list(map(ord, tuple(other_box_id)))))
                if len([1 for value in common if value != 0]) == 1:

                    print(f"Found correct ID: {box_id}")
                    return

def main():
    box_ids = read_box_ids()
    find_common_letters(box_ids)


if __name__ == "__main__":
    sys.exit(main())
