#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from enum import Enum

import sys
from typing import NamedTuple, Deque, List

INPUT_FILE = "input.txt"
NUMBER_OF_MOVES = 100


class Player(NamedTuple):
    x: int
    y: int


@dataclass(eq=True)
class Player:
    name: str
    deck: Deque[int]


def get_pickup_cups(current_cup: int, cups: List[int]) -> List[int]:
    current_cup_index = cups.index(current_cup)
    picked_up = list()
    if current_cup_index < len(cups) - 4:
        picked_up = list(cups[current_cup_index + 1 : current_cup_index + 4])
    elif current_cup_index == len(cups) - 1:
        picked_up = list(cups[:3])
    elif current_cup_index == len(cups) - 3:
        picked_up = list(cups[current_cup_index + 1 :])
        picked_up.append(cups[0])
    elif current_cup_index == len(cups) - 2:
        picked_up = list(cups[current_cup_index + 1 :])
        picked_up.append(cups[0])
        picked_up.append(cups[1])
    return picked_up


def get_destination_cup(
    current_cup: int, cups: List[int], pickup_cups: List[int]
) -> int:
    destination_cup = current_cup - 1
    if destination_cup in pickup_cups:
        while True:
            destination_cup -= 1
            if destination_cup < min(set(cups).difference(pickup_cups)):
                destination_cup = max(set(cups).difference(pickup_cups))
                break
            if destination_cup in pickup_cups:
                continue
            else:
                break
    return destination_cup


def insert_back_pickup_cups(
    current_cup: int, destination_cup: int, cups: List[int], pickup_cups: List[int]
):
    if cups.index(pickup_cups[0]) < 3:
        del cups[cups.index(pickup_cups[0]) : cups.index(pickup_cups[0]) + 3]
        for index, cup in enumerate(pickup_cups, start=1):
            cups.insert(cups.index(destination_cup) + index, cup)
    else:
        cups.append(cups[0])


def play_game(cups: List[int]) -> None:
    cups = deque(cups)

    for _ in range(100):
        orig_val = cups[0]
        dest_val = cups[0] - 1
        if dest_val < 1:
            dest_val += 9
        cups.rotate(-1)

        c1 = cups.popleft()
        c2 = cups.popleft()
        c3 = cups.popleft()

        while dest_val in (c1, c2, c3):
            dest_val = dest_val - 1 if dest_val > 1 else dest_val + 8

        while cups[0] != dest_val:
            cups.rotate(-1)
        cups.rotate(-1)

        cups.append(c1)
        cups.append(c2)
        cups.append(c3)

        while cups[0] != orig_val:
            cups.rotate(-1)
        cups.rotate(-1)

    while cups[0] != 1:
        cups.rotate(-1)
    cups.popleft()

    print(''.join([str(i) for i in cups]))
    """
    current_cup = cups[0]
    for _ in range(3):
        pickup_cups = get_pickup_cups(current_cup, cups)
        print(f"PICKEUP CUPS: {pickup_cups}")
        destination_cup = get_destination_cup(current_cup, cups, pickup_cups)
        print(f"DESTINATION CUP: {destination_cup}")
        insert_back_pickup_cups(current_cup, destination_cup, cups, pickup_cups)
        current_cup = cups[cups.index(current_cup) + 1]
        print(f"CURRENT CUP: {current_cup}")
        print(cups)
    """


def read_cups() -> List[int]:
    cups = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                cups = [int(number) for number in line]
    return cups


def main():
    cups = read_cups()
    play_game(cups)


if __name__ == "__main__":
    sys.exit(main())
