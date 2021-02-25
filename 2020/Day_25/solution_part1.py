#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum

import sys
from typing import Deque

INPUT_FILE = "input.txt"
REFERENCE_TILE = (0, 0)

BLACK, WHITE = (0, 1)


class Direction(Enum):
    EAST = "e"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    WEST = "w"
    NORTHWEST = "nw"
    NORTHEAST = "ne"


DIRECTION_SLOPES = {
    "e": (1, 0),
    "se": (0.5, -0.5),
    "sw": (-0.5, -0.5),
    "w": (-1, 0),
    "nw": (-0.5, 0.5),
    "ne": (0.5, 0.5),
}


@dataclass
class PublicKeys:
    card: int = 0
    door: int = 0


@dataclass(eq=True)
class Player:
    name: str
    deck: Deque[int]


def find_secret_loop_size(public_key: int) -> int:
    value = 1
    subject_number = 7
    count = 1
    while True:
        value = value * subject_number
        value = value % 20201227
        if value == public_key:
            break
        count += 1
    return count


def produce_encryption_key(subject_number: int, loop_size) -> int:
    value = 1
    for _ in range(loop_size):
        value = value * subject_number
        value = value % 20201227
    return value


def find_encryption_key(keys: PublicKeys):
    card_secret_loop_size = find_secret_loop_size(public_key=keys.card)
    door_secret_loop_size = find_secret_loop_size(public_key=keys.door)
    encryption_key_1 = produce_encryption_key(keys.card, door_secret_loop_size)
    encryption_key_2 = produce_encryption_key(keys.door, card_secret_loop_size)
    if encryption_key_1 == encryption_key_2:
        print(f"Found correct encryption key: {encryption_key_2}")


def read_public_keys() -> PublicKeys:
    public_keys = PublicKeys()
    with open(INPUT_FILE, "r") as f_handle:
        lines = f_handle.readlines()
        public_keys.card = int(lines[0].rstrip())
        public_keys.door = int(lines[1].rstrip())
    return public_keys


def main():
    keys = read_public_keys()
    find_encryption_key(keys)


if __name__ == "__main__":
    sys.exit(main())
