#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math

INPUT_FILE = "input.txt"
inputs = []


def read_inputs():
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            inputs.append(int(line.strip()))


def calculate_total_fuel_consumption():
    return sum(math.floor(mass / 3.0) - 2 for mass in inputs)


def main():
    read_inputs()
    print(calculate_total_fuel_consumption())


if __name__ == "__main__":
    sys.exit(main())
