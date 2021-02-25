#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import math
import sys
from typing import Set

INPUT_FILE = "input.txt"

UPPER_ROW_HALF, LOWER_ROW_HALF = ("B", "F")
UPPER_COLUMN_HALF, LOWER_COLUMN_HALF = ("R", "L")


@dataclass(frozen=True, eq=True)
class BoardingPass:
    seat_id: str


def find_row_index(seat_id):
    row_range = range(0, 128)
    return find_index(row_range, seat_id)


def find_column_index(seat_id):
    row_range = range(0, 8)
    return find_index(row_range, seat_id)


def find_index(array, ids):
    mid_point = 0
    for half in ids:
        try:
            mid_point = range_mid_point(array, half)
            if half in (UPPER_ROW_HALF, UPPER_COLUMN_HALF):
                array = array[mid_point:]
            if half in (LOWER_ROW_HALF, LOWER_COLUMN_HALF):
                array = array[: mid_point + 1]
        except IndexError as e:
            print(e)
    if len(array) == 1:
        return array[0]
    return array[mid_point]


def range_mid_point(array: range, part: str) -> int:
    try:
        if part in (LOWER_ROW_HALF, LOWER_COLUMN_HALF):
            return math.floor((array[-1] - array[0]) / 2)
        if part in (UPPER_ROW_HALF, UPPER_COLUMN_HALF):
            return math.ceil((array[-1] - array[0]) / 2)
    except IndexError:
        print(array)


def read_boarding_passes() -> Set[BoardingPass]:
    boarding_passes = set()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                boarding_passes.add(BoardingPass(seat_id=line.rstrip()))
    return boarding_passes


def calculate_max_seat_id(boarding_passes: Set[BoardingPass]):
    max_id = -1
    for boarding_pass in boarding_passes:
        row_id = boarding_pass.seat_id[:-3]
        column_id = boarding_pass.seat_id[-3:]
        row_number = find_row_index(row_id)
        column_number = find_column_index(column_id)
        max_id = max(max_id, row_number * 8 + column_number)
    return max_id


def main():
    boarding_passes = read_boarding_passes()
    print(calculate_max_seat_id(boarding_passes))


if __name__ == "__main__":
    sys.exit(main())
