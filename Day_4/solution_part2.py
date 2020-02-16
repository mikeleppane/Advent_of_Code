#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
from typing import NamedTuple
from itertools import groupby

INPUT_FILE = "input.txt"


class PasswordRange(NamedTuple):
    lower: str
    upper: str


def read_password_range():
    with open(INPUT_FILE, "r") as f_handle:
        return PasswordRange(*f_handle.readline().strip().split("-"))


def find_possible_passwords(_range):
    possible_passwords = 0
    for number in range(int(_range.lower), int(_range.upper) + 1):
        number_str = str(number)
        if number_str == "".join(sorted(number_str)):
            if is_part_of_larger_group(number_str):
                possible_passwords += 1
    return possible_passwords


def is_part_of_larger_group(number):
    groups = [list(g) for k, g in groupby(number)]
    if any(len(elem) == 3 and len(groups) != 3 for elem in groups):
        return False
    if len(groups) == 1:
        return False
    if len(groups) == 3:
        if all(len(elem) == 2 for elem in groups):
            return True
        if all(len(elem) in (1, 2, 3) for elem in groups):
            return True
        return False
    if len(groups) == 2:
        if len(groups[0]) in (2, 4):
            return True
        return False

    if len(groups) == 6:
        return False
    if len(groups) in (4, 5):
        return True
    return True


def main():
    _range = read_password_range()
    print(find_possible_passwords(_range))


if __name__ == "__main__":
    sys.exit(main())
