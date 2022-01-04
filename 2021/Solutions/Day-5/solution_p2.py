#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from dataclasses import dataclass
from pprint import PrettyPrinter
from typing import List, Tuple

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
EMPTY_CELL = "."


@dataclass
class Line:
    x1: int
    x2: int
    y1: int
    y2: int


def fill_diagram_with_lines(lines: List[Line], diagram: np.ndarray) -> np.ndarray:
    for line in lines:
        if line.x1 == line.x2:
            y1 = min(line.y1, line.y2)
            y2 = max(line.y1, line.y2)
            for yi in range(y1, y2 + 1):
                if diagram[yi, line.x1] == EMPTY_CELL:
                    diagram[yi, line.x1] = "1"
                else:
                    diagram[yi, line.x1] = f"{int(diagram[yi, line.x1]) + 1}"
        elif line.y1 == line.y2:
            x1 = min(line.x1, line.x2)
            x2 = max(line.x1, line.x2)
            for xi in range(x1, x2 + 1):
                if diagram[line.y1, xi] == EMPTY_CELL:
                    diagram[line.y1, xi] = "1"
                else:
                    diagram[line.y1, xi] = f"{int(diagram[line.y1, xi]) + 1}"
        else:
            xdir = 1
            ydir = 1
            if line.x1 > line.x2:
                xdir = -1
            if line.y1 > line.y2:
                ydir = -1
            xr = line.x1
            yr = line.y1
            for _ in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
                if diagram[yr, xr] == EMPTY_CELL:
                    diagram[yr, xr] = "1"
                else:
                    diagram[yr, xr] = f"{int(diagram[yr, xr]) + 1}"
                xr += xdir
                yr += ydir
    return diagram


def read_lines_of_vents() -> Tuple[List[Line], int, int]:
    lines: List[Line] = []
    vent_line_regex = re.compile(r"""(\d*)[,](\d*)\s+->\s+(\d*)[,](\d*)""")
    max_x = 0
    max_y = 0
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                if match := vent_line_regex.match(line):
                    x1, y1, x2, y2 = match.groups()
                    max_x = max(max_x, int(x1), int(x2))
                    max_y = max(max_y, int(y1), int(y2))
                    lines.append(Line(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2)))
    return lines, max_x, max_y


def create_diagram(max_x: int, max_y: int) -> np.ndarray:
    return np.full([max_y + 1, max_x + 1], fill_value=EMPTY_CELL, dtype=str)


def calculate_number_of_overlaps(new_diagram: np.ndarray) -> int:
    overlaps = 0
    for x in np.nditer(new_diagram.flatten()):
        if x != '.' and int(x) >= 2:
            overlaps += 1
    return overlaps


def solve() -> int:
    lines, max_x, max_y = read_lines_of_vents()
    diagram = create_diagram(max_x, max_y)
    new_diagram = fill_diagram_with_lines(lines, diagram)
    return calculate_number_of_overlaps(new_diagram)


def main():
    number_of_overlaps = solve()
    print(f"Result: {number_of_overlaps}")


if __name__ == "__main__":
    sys.exit(main())
