#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from dataclasses import dataclass
from pprint import PrettyPrinter
from typing import Dict, List, NamedTuple

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"
MAX_GRID_SIZE = 10


class Point(NamedTuple):
    i: int
    j: int


@dataclass
class Octopus:
    energy_level: int
    has_flashed: bool


def read_energy_levels() -> Dict[Point, Octopus]:
    energy_levels: Dict[Point, Octopus] = {}
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for row, line in enumerate(f_handle):
            line = line.rstrip()
            if line:
                for column, energy_level in enumerate(list(line)):
                    energy_levels.update(
                        {
                            Point(column, row): Octopus(
                                energy_level=int(energy_level), has_flashed=False
                            )
                        }
                    )
    return energy_levels


def get_adjacent_points(point: Point) -> List[Point]:
    adjacent_points = [
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
    ]
    new_points: List[Point] = []
    for adjacent_point in adjacent_points:
        x = adjacent_point[0] + point.i
        y = adjacent_point[1] + point.j
        if 0 <= x <= 9 and 0 <= y <= 9:
            new_points.append(Point(x, y))
    return new_points


def start_simulation(energy_levels: Dict[Point, Octopus], steps=100) -> int:
    flash_counter = 0
    for _ in range(0, steps):
        for octopus in energy_levels.values():
            octopus.energy_level += 1
        while True:
            has_energy_level_above_9 = False
            for point, octopus in energy_levels.items():
                if octopus.energy_level > 9 and not octopus.has_flashed:
                    has_energy_level_above_9 = True
                    octopus.has_flashed = True
                    flash_counter += 1
                    for adjacent_point in get_adjacent_points(point):
                        energy_levels[adjacent_point].energy_level += 1
            if not has_energy_level_above_9:
                break
        for octopus in energy_levels.values():
            if octopus.has_flashed:
                octopus.energy_level = 0
                octopus.has_flashed = False
    return flash_counter


def solve() -> int:
    energy_levels = read_energy_levels()
    return start_simulation(energy_levels)


def main():
    number_of_flashes = solve()
    print(f"Result: {number_of_flashes}")


if __name__ == "__main__":
    sys.exit(main())
