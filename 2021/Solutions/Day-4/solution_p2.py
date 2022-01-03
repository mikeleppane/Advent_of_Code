#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
BOARD_SIZE = 5


def calculate_final_score(board: np.matrix, drawn_numbers: List[int]) -> int:
    unmarked_numbers = []
    for number in np.nditer(board.flatten()):
        if number not in drawn_numbers:
            unmarked_numbers.append(number)
    return sum(unmarked_numbers) * drawn_numbers[-1]


def find_board_which_wins_last(boards, numbers):
    drawn_numbers = numbers[0:5]
    winning_boards = []
    for number in numbers[5:]:
        for board_index, board in enumerate(boards):
            for index in range(BOARD_SIZE):
                bingo_on_row = (
                        np.size(
                            np.intersect1d(
                                np.array(board[index, :]), np.array(drawn_numbers)
                            )
                        )
                        == BOARD_SIZE
                )
                bingo_on_column = (
                        np.size(
                            np.intersect1d(
                                np.array(board[:, index]), np.array(drawn_numbers)
                            )
                        )
                        == BOARD_SIZE
                )
                if bingo_on_column or bingo_on_row:
                    print(f"BINGO on board {board_index}")
                    if board_index not in winning_boards:
                        winning_boards.append(board_index)
                    if len(winning_boards) == len(boards):
                        return boards[winning_boards[-1]], drawn_numbers
        drawn_numbers.append(number)


def read_bingo_input() -> Tuple[List[np.matrix], List[int]]:
    numbers: List[int] = []
    boards: List[np.matrix] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        board = []
        for index, line in enumerate(f_handle):
            line = line.rstrip()
            if line:
                if index == 0:
                    numbers = [int(num) for num in line.split(",")]
                    continue
                else:
                    board.append([int(num) for num in line.split(" ") if num.strip()])
            else:
                if board:
                    boards.append(np.matrix(board))
                board = []
        if board:
            boards.append(np.matrix(board))
    return boards, numbers


def solve() -> int:
    boards, numbers = read_bingo_input()
    winning_board, drawn_numbers = find_board_which_wins_last(boards, numbers)
    return calculate_final_score(winning_board, drawn_numbers)


def main():
    final_score = solve()
    print(f"Result: {final_score}")


if __name__ == "__main__":
    sys.exit(main())
