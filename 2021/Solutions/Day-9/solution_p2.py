#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass
from functools import reduce
from pprint import PrettyPrinter
from typing import Dict, List, Set

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


@dataclass(unsafe_hash=True, eq=True)
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


def get_valid_adjacent_points(point: Point, heightmap: np.ndarray) -> List[Point]:
    up, down, left, right = (1, 1, 1, 1)
    adjacent_points: List[Point] = []
    i_max, j_max = heightmap.shape
    non_valid_basin = 9
    if (
            point.i - left >= 0
            and heightmap[point.i - left, point.j].item() < non_valid_basin
    ):
        adjacent_points.append(
            Point(
                point.i - left,
                j=point.j,
                value=heightmap[point.i - left, point.j].item(),
            )
        )
    if (
            point.i + right <= i_max - 1
            and heightmap[point.i + right, point.j].item() < non_valid_basin
    ):
        adjacent_points.append(
            Point(
                point.i + right,
                j=point.j,
                value=heightmap[point.i + right, point.j].item(),
            )
        )
    if point.j - up >= 0 and heightmap[point.i, point.j - up].item() < non_valid_basin:
        adjacent_points.append(
            Point(
                point.i, j=point.j - up, value=heightmap[point.i, point.j - up].item()
            )
        )
    if (
            point.j + down <= j_max - 1
            and heightmap[point.i, point.j + down].item() < non_valid_basin
    ):
        adjacent_points.append(
            Point(
                point.i,
                j=point.j + down,
                value=heightmap[point.i, point.j + down].item(),
            )
        )
    return adjacent_points


def find_basins(low_point: Point, heightmap: np.ndarray, visited_points: Set[Point]):
    for point in get_valid_adjacent_points(low_point, heightmap):
        if point not in visited_points:
            visited_points.add(point)
            find_basins(point, heightmap, visited_points)


def calculate_size_of_top_3_basins(basins: Dict[Point, Set[Point]]) -> int:
    return reduce(
        lambda a, b: a * b,
        sorted([len(basin_size) for basin_size in basins.values()], reverse=True)[0:3],
    )


def solve() -> int:
    heightmap = read_heightmap()
    low_points = find_low_points_from_map(heightmap)
    basins = {}
    for low_point in low_points:
        visited_points: Set[Point] = set()
        find_basins(low_point, heightmap, visited_points)
        basins[low_point] = visited_points
    return calculate_size_of_top_3_basins(basins)


def main():
    size_of_top_3_basins = solve()
    print(f"Result: {size_of_top_3_basins}")


if __name__ == "__main__":
    sys.exit(main())
