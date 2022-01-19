#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter

import sys
from pprint import PrettyPrinter
from typing import List, Set, Tuple

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "test_input_3.txt"


def read_map() -> List[List[str]]:
    caves: List[List[str]] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                caves.append(line.split("-"))
    return caves


def contain_twice_visited_small_cave(path: List[str]) -> bool:
    return Counter([char for char in path if char.islower()]).most_common(1)[0][1] > 1


def should_append_next_cave(next_cave: str, path: List[str]) -> bool:
    if next_cave != path[-1]:
        if next_cave.islower():
            if path.count(next_cave) == 0:
                return True
            if path.count(next_cave) == 1 and not contain_twice_visited_small_cave(
                    path
            ):
                return True
        if next_cave.isupper():
            return True
    return False


def find_distinct_paths(
        name, caves: List[List[str]], path: List[str], paths: Set[Tuple[str, ...]]
):
    for cave in caves:
        if name in cave:
            next_cave = get_next_cave(name, cave)
            if next_cave == "end":
                new_path: Tuple[str, ...] = (*path, "end")
                if new_path not in paths:
                    paths.add(new_path)
            elif should_append_next_cave(next_cave, path):
                path.append(next_cave)
                find_distinct_paths(next_cave, caves, path, paths)
    if len(path) > 2:
        path.pop()


def get_next_cave(name, cave: List[str]) -> str:
    next_index = 1 if cave.index(name) == 0 else 0
    return cave[next_index]


def solve() -> int:
    caves = read_map()
    start_caves = [cave for cave in caves if "start" in cave]
    other_caves = [cave for cave in caves if "start" not in cave]
    paths: Set[Tuple[str, ...]] = set()
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
