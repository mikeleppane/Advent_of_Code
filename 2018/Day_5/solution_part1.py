#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from collections import deque
INPUT_FILE = "input.txt"


def scan_polymer(polymer: str):
    while True:
        indices_to_be_removed = set()
        found = False
        for index in range(len(polymer) - 1):
            if (polymer[index].isupper() and polymer[index + 1].islower()) or (
                polymer[index].islower() and polymer[index + 1].isupper()
            ):
                if polymer[index].lower() == polymer[index + 1].lower():
                    found = True
                    indices_to_be_removed.add(index)
                    indices_to_be_removed.add(index + 1)
                    polymer = polymer.replace(polymer[index] + polymer[index + 1], "")
                    break
        if not found:
            break
    print("".join(polymer))
    print(len(polymer))


def read_polymer() -> str:
    polymer = ""
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                polymer += line.rstrip()

    return polymer


def main():
    polymer = read_polymer()
    scan_polymer(polymer)


if __name__ == "__main__":
    sys.exit(main())
