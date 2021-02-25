#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import Counter


INPUT_FILE = "input.txt"


def calculate_sum_of_yes_counts():
    yes_count = list()
    group = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                answers = set()
                for char in line:
                    answers.add(char)
                group.append(answers)
            if not line:
                if len(group) == 1:
                    yes_count.append(len(group[0]))
                else:
                    c = Counter()
                    for item in group:
                        for subitem in item:
                            c[subitem] += 1
                    for key, value in c.most_common():
                        if value == len(group):
                            yes_count.append(1)
                group.clear()
    if len(group) == 1:
        yes_count.append(len(group[0]))
    else:
        c = Counter()
        for item in group:
            for subitem in item:
                c[subitem] += 1
        for key, value in c.most_common():
            if value == len(group):
                yes_count.append(1)
    print(sum(yes_count))


def main():
    calculate_sum_of_yes_counts()


if __name__ == "__main__":
    sys.exit(main())
