#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import defaultdict

import sys
from typing import List

INPUT_FILE = "input.txt"

metadata_entries = list()


def scan_child_nodes(number_of_child_nodes, license_file):
    if not license_file:
        return
    node_values = defaultdict(int)
    for i in range(1, number_of_child_nodes + 1):
        number_child_nodes = license_file.pop(0)
        number_of_metadata_entries = license_file.pop(0)
        if number_child_nodes > 0:
            nd = scan_child_nodes(number_child_nodes, license_file)
            for metadata in license_file[:number_of_metadata_entries]:
                if metadata in nd:
                    node_values[i] += nd[metadata]
                else:
                    node_values[i] += 0
        else:
            node_values[i] = sum(license_file[:number_of_metadata_entries])
        for metadata in license_file[:number_of_metadata_entries]:
            metadata_entries.append(metadata)
        del license_file[:number_of_metadata_entries]
    return node_values


def scan_license_file(license_file: List[int]):
    while license_file:
        number_child_nodes = license_file.pop(0)
        number_of_metadata_entries = license_file.pop(0)
        if number_child_nodes > 0:
            node_values = scan_child_nodes(number_child_nodes, license_file)
        for metadata in license_file[:number_of_metadata_entries]:
            metadata_entries.append(metadata)
        del license_file[:number_of_metadata_entries]
    print(node_values)
    print(metadata_entries[-11:])
    t = 0
    for i in metadata_entries[-11:]:
        if i in node_values:
            t += node_values[i]
    print(t)


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
