#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict, deque
from typing import Deque, List

INPUT_FILE = "input.txt"
FINAL_SPOKEN_NUMBER = 30000000


def memory_game(starting_numbers: Deque[int]) -> None:
    game_turns = defaultdict(list)
    turn = 1
    last_spoken_number = 0
    while True:
        if starting_numbers:
            last_spoken_number = starting_numbers.popleft()
            game_turns[last_spoken_number].append(turn)
        else:
            if len(game_turns[last_spoken_number]) == 1:
                last_spoken_number = 0
                game_turns[0].append(turn)
            elif len(game_turns[last_spoken_number]) > 1:
                last_spoken_numbers = game_turns[last_spoken_number]
                last_spoken_number = last_spoken_numbers[-1] - last_spoken_numbers[-2]
                game_turns[last_spoken_number].append(turn)
        if turn == FINAL_SPOKEN_NUMBER:
            print(last_spoken_number)
            return
        turn += 1


def read_starting_numbers() -> List[int]:
    numbers = list()
    with open(INPUT_FILE, "r") as f_handle:
        for index, line in enumerate(f_handle):
            numbers = [
                int(number) for number in line.rstrip().split(",") if number.isdigit()
            ]
    return numbers


def main():
    numbers = deque(read_starting_numbers())
    memory_game(numbers)


if __name__ == "__main__":
    sys.exit(main())
