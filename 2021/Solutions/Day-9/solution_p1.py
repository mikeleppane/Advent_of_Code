#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from dataclasses import dataclass
from pprint import PrettyPrinter
from typing import List

import numpy as np

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"


@dataclass
class Point:
    i: int
    j: int
    value: int = -1


def read_heightmap() -> np.ndarray:
    heightmap: List[List[int]] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                heightmap.append([int(num) for num in list(line)])
    return np.asarray(heightmap)


def find_low_points_from_map(heightmap: np.ndarray) -> List[Point]:
    low_points: List[Point] = []
    it: np.nditer = np.nditer(heightmap, flags=["multi_index"])
    i_max, j_max = heightmap.shape
    up, down, left, right = (1, 1, 1, 1)
    for xr in it:
        x: int = xr.item()
        adjacent_points: List[bool] = []
        i, j = it.multi_index
        if i - left >= 0:
            adjacent_points.append(x < heightmap[i - left, j])
        if i + right <= i_max - 1:
            adjacent_points.append(x < heightmap[i + right, j])
        if j - up >= 0:
            adjacent_points.append(x < heightmap[i, j - up])
        if j + down <= j_max - 1:
            adjacent_points.append(x < heightmap[i, j + down])
        if all(adjacent_points):
            low_points.append(Point(i=i, j=j, value=x))

    return low_points


def calculate_risk_level(low_points: List[Point]) -> int:
    return sum((point.value + 1 for point in low_points))


def solve() -> int:
    heightmap = read_heightmap()
    low_points = find_low_points_from_map(heightmap)
    return calculate_risk_level(low_points)


def main():
    risk_level = solve()
    print(f"Result: {risk_level}")


if __name__ == "__main__":
    sys.exit(main())
