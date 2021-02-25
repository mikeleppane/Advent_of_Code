#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

import re
import sys
from pprint import PrettyPrinter
from typing import Tuple, List

INPUT_FILE = "input.txt"


pp = PrettyPrinter(indent=4)


@dataclass
class Nanobot:
    x: int
    y: int
    z: int
    r: int


def manhattan(p1: Nanobot, p2: Nanobot):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)


def find_largest_nanobot(nanobots: List[Nanobot]) -> Nanobot:
    return sorted(nanobots, key=lambda nanobot: nanobot.r, reverse=True)[0]


def find_closest_nanobots(nanobots: List[Nanobot]):
    largest_nanobot = find_largest_nanobot(nanobots)
    largest_nanobot_index = nanobots.index(largest_nanobot)
    nanobots.remove(largest_nanobot)
    count = 1
    for nanobot in nanobots:
        if manhattan(largest_nanobot, nanobot) <= largest_nanobot.r:
            count += 1

    print(count)


def read_nanobots() -> List[Nanobot]:
    nanobots = list()
    position_regex = re.compile(
        r"pos=<([-]?\d{1,12}),([-]?\d{1,12}),([-]?\d{1,12})>\, r=(\d{1,12})"
    )
    radius_regex = re.compile(r"\.*r=(\d{1,10})")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                x, y, z, r = list(map(int, position_regex.match(line).groups()))
                nanobots.append(Nanobot(x=x, y=y, z=z, r=r))
    return nanobots


def main():
    nanobots = read_nanobots()
    print(
        sorted(
            nanobots,
            key=lambda nanobot: manhattan(nanobot, Nanobot(x=0, y=0, z=0, r=0)),
        )[0]
    )
    # find_closest_nanobots(nanobots)


if __name__ == "__main__":
    sys.exit(main())
