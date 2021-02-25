#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
import sys
from typing import List
from collections import deque
from boltons.iterutils import flatten

INPUT_FILE = "input.txt"

metadata_entries = list()


def scan_child_nodes(number_of_child_nodes, license_file):
    if not license_file:
        return
    for _ in range(number_of_child_nodes):
        number_child_nodes = license_file.pop(0)
        number_of_metadata_entries = license_file.pop(0)
        if number_child_nodes > 0:
            scan_child_nodes(number_child_nodes, license_file)
        for metadata in license_file[:number_of_metadata_entries]:
            metadata_entries.append(metadata)
        del license_file[:number_of_metadata_entries]


def scan_license_file(license_file: List[int]):
    while license_file:
        number_child_nodes = license_file.pop(0)
        number_of_metadata_entries = license_file.pop(0)
        if number_child_nodes > 0:
            scan_child_nodes(number_child_nodes, license_file)
        for metadata in license_file[:number_of_metadata_entries]:
            metadata_entries.append(metadata)
        del license_file[:number_of_metadata_entries]
    print(sum(metadata_entries))


def read_license_file() -> List[int]:
    license_file = []
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                license_file = list(map(int, line.split(" ")))

    return license_file


def main():
    license_file = read_license_file()
    scan_license_file(license_file)


if __name__ == "__main__":
    sys.exit(main())
