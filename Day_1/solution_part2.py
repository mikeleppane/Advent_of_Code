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


def calculate_total_fuel_required_for_module(module_mass):
    total_fuel = 0
    while True:
        module_mass = math.floor(module_mass / 3.0)
        if module_mass == 0 or (module_mass - 2) <= 0:
            break
        module_mass -= 2
        total_fuel += module_mass
    return total_fuel


def calculate_total_fuel_consumption():
    return sum(calculate_total_fuel_required_for_module(mass) for mass in inputs)


def main():
    read_inputs()
    print(calculate_total_fuel_consumption())


if __name__ == "__main__":
    sys.exit(main())
