#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
from typing import NamedTuple

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
            for index, value in enumerate(number_str):
                try:
                    if value == number_str[index + 1]:
                        possible_passwords += 1
                        break
                except (KeyError, IndexError):
                    pass
    return possible_passwords


def main():
    _range = read_password_range()
    print(find_possible_passwords(_range))


if __name__ == "__main__":
    sys.exit(main())
