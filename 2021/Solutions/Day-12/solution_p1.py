#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pprint import PrettyPrinter
from typing import List

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"


def read_map() -> List[List[str]]:
    caves: List[List[str]] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                caves.append(line.split("-"))
    return caves


def find_distinct_paths(
        name, caves: List[List[str]], path: List[str], paths: List[List[str]]
):
    for cave in caves:
        if name in cave:
            next_cave = get_next_cave(name, cave)
            if next_cave == "end":
                new_path = path.copy()
                new_path.append("end")
                if new_path not in paths:
                    paths.append(new_path)
            elif (
                    (next_cave.islower() and next_cave not in path)
                    or next_cave.isupper()
                    and next_cave != path[-1]
            ):
                path.append(next_cave)
                find_distinct_paths(next_cave, caves, path, paths)
    path.pop()


def get_next_cave(name, cave: List[str]) -> str:
    next_index = 1 if cave.index(name) == 0 else 0
    return cave[next_index]


def solve() -> int:
    caves = read_map()
    start_caves = [cave for cave in caves if "start" in cave]
    other_caves = [cave for cave in caves if "start" not in cave]
    paths: List[List[str]] = []
    for start_cave in start_caves:
        path: List[str] = ["start"]
        next_cave = get_next_cave("start", start_cave)
        path.append(next_cave)
        find_distinct_paths(next_cave, other_caves, path, paths)
    return len(paths)


def main():
    number_of_paths = solve()
    print(f"Result: {number_of_paths}")


if __name__ == "__main__":
    sys.exit(main())
