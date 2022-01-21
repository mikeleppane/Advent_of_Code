#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
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


def count_visible_dots_after_first_fold(
    paper: np.ndarray, folds: List[Tuple[str, int]]
) -> int:
    new_paper = paper.copy()
    axis, number = folds[0]
    if axis == "y":
        new_paper = new_paper[0:number, 0:] + np.flipud(new_paper[number + 1 :, 0:])
        new_paper = np.where(new_paper == 2, 1, new_paper)
    elif axis == "x":
        new_paper = np.fliplr(new_paper[0:, 0:number]) + new_paper[0:, number + 1 :]
        new_paper = np.where(new_paper == 2, 1, new_paper)
    return np.count_nonzero(new_paper == 1)


def read_instructions() -> Tuple[np.ndarray, List[Tuple[str, int]]]:
    folds: List[Tuple[str, int]] = []
    points: List[List[int, int]] = []
    x_max, y_max = 0, 0
    fold_along_regex = re.compile(r"^fold along\s+(x|y)+=(\d+)")
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                if "fold along" in line and (m := fold_along_regex.match(line)):
                    folds.append((m.group(1), int(m.group(2))))
                else:
                    x, y = [int(number) for number in line.split(",")]
                    x_max = max(x, x_max)
                    y_max = max(y, y_max)
                    points.append([x, y])
    paper = np.zeros((y_max + 1, x_max + 1), dtype=int)
    for point in points:
        paper[point[1], point[0]] = 1

    return paper, folds


def solve() -> int:
    paper, folds = read_instructions()
    return count_visible_dots_after_first_fold(paper, folds)


def main():
    number_of_dots = solve()
    print(f"Result: {number_of_dots}")


if __name__ == "__main__":
    sys.exit(main())
