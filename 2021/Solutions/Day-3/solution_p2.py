#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import numpy as np

INPUT_FILE = "input.txt"


def convert_bit_array_to_int(array: np.ndarray) -> int:
    return int("".join((str(num) for num in np.nditer(array[:]))), 2)


def find_oxygen_generator_rating(report: np.matrix) -> int:
    _, columns = report.shape
    for index in range(0, columns):
        rows, _ = report.shape
        if rows == 1:
            break
        nbr_of_ones = np.size(np.where(report[:, index] == 1)[0])
        nbr_of_zeros = rows - nbr_of_ones
        if nbr_of_ones >= nbr_of_zeros:
            report = report[np.where(report[:, index] == 1)[0], :]
        else:
            report = report[np.where(report[:, index] == 0)[0], :]
    return convert_bit_array_to_int(report)


def find_co2_scrubber_rating(report: np.matrix) -> int:
    _, columns = report.shape
    for index in range(0, columns):
        rows, _ = report.shape
        if rows == 1:
            break
        nbr_of_zeros = np.size(np.where(report[:, index] == 0)[0])
        nbr_of_ones = rows - nbr_of_zeros
        if nbr_of_zeros <= nbr_of_ones:
            report = report[np.where(report[:, index] == 0)[0], :]
        else:
            report = report[np.where(report[:, index] == 1)[0], :]
    return convert_bit_array_to_int(report)


def read_diagnostic_report() -> np.matrix:
    report = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            row = []
            if line:
                for char in line.rstrip():
                    row.append(int(char))
                report.append(row)
    return np.matrix(report)


def solve():
    report = read_diagnostic_report()
    oxygen_generator_rating = find_oxygen_generator_rating(
        np.matrix(report, copy=True)
    )
    co2_scrubber_rating = find_co2_scrubber_rating(np.matrix(report, copy=True))
    solution = oxygen_generator_rating * co2_scrubber_rating
    return solution


def main():
    solution = solve()
    print(f"Result: {solution}")


if __name__ == "__main__":
    sys.exit(main())
