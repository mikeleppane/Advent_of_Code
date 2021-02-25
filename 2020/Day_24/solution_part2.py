#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import add
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import sys
from pprint import PrettyPrinter
from typing import NamedTuple, Deque, List, Dict

INPUT_FILE = "input.txt"
REFERENCE_TILE = (0, 0)
NUMBER_OF_DAYS = 100
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
    "se": (0.5, -1),
    "sw": (-0.5, -1),
    "w": (-1, 0),
    "nw": (-0.5, 1),
    "ne": (0.5, 1),
}
DIRECTION_SLOPES_2 = {
    "e": (1, 0),
    "se": (1, -1),
    "se_2": (0.5, -0.5),
    "sw": (-1, -1),
    "sw_2": (-0.5, -0.5),
    "w": (-1, 0),
    "nw": (-1, 1),
    "nw_2": (-0.5, 0.5),
    "ne": (1, 1),
    "ne_2": (0.5, 0.5),
}

class Player(NamedTuple):
    x: int
    y: int


@dataclass(eq=True)
class Player:
    name: str
    deck: Deque[int]


def process_crew_list(tiles: Dict[int, List[str]]):
    pp = PrettyPrinter(indent=4)
    visited_tiles = dict()
    for tile_number, route in tiles.items():
        destination_tile = REFERENCE_TILE
        for direction in route:
            destination_tile = tuple(
                map(add, destination_tile, DIRECTION_SLOPES[direction])
            )
        if destination_tile not in visited_tiles:
            visited_tiles.update({destination_tile: BLACK})
        else:
            visited_tiles[destination_tile] = visited_tiles[destination_tile] ^ 1
    for _ in range(100):
        prev_tiles = deepcopy(visited_tiles)
        #pp.pprint(visited_tiles)
        for destination_tile, color in prev_tiles.items():
            if color == BLACK:
                count = 0
                for d in DIRECTION_SLOPES.values():
                    tf = tuple(map(add, destination_tile, d))
                    if tf in prev_tiles and prev_tiles[tf] == BLACK:
                        count += 1
                    if tf not in prev_tiles:
                        ct = 0
                        for d2 in DIRECTION_SLOPES.values():
                            tf_2 = tuple(map(add, tf, d2))
                            if tf_2 in prev_tiles and prev_tiles[tf_2] == BLACK:
                                ct += 1
                        if ct == 2:
                            visited_tiles.update({tf: BLACK})
                if count == 0 or count > 2:
                    #print(f"DESTINATION TILE: {destination_tile}")
                    visited_tiles[destination_tile] = WHITE
            if color == WHITE:
                count = 0
                for d in DIRECTION_SLOPES.values():
                    tf = tuple(map(add, destination_tile, d))
                    if tf in prev_tiles and prev_tiles[tf] == BLACK:
                        count += 1
                    if tf not in prev_tiles:
                        ct = 0
                        for d2 in DIRECTION_SLOPES.values():
                            tf_2 = tuple(map(add, tf, d2))
                            if tf_2 in prev_tiles and prev_tiles[tf_2] == BLACK:
                                ct += 1
                        if ct == 2:
                            visited_tiles.update({tf: BLACK})
                if count == 2:
                    visited_tiles[destination_tile] = BLACK
    count = 0
    for tile_side in visited_tiles.values():
        if tile_side == BLACK:
            count += 1
    print(count)


def read_tiles() -> Dict[int, List[str]]:
    tiles = dict()
    directions = {direction.value for direction in Direction}
    with open(INPUT_FILE, "r") as f_handle:
        for line_number, line in enumerate(f_handle, start=1):
            line = line.rstrip()
            if line:
                tiles[line_number] = list()
                while len(line):
                    index = 0
                    if line[index] in directions:
                        tiles[line_number].append(line[index])
                        line = line[1:]
                    if line[index : index + 2] in directions:
                        tiles[line_number].append(line[index : index + 2])
                        line = line[2:]
    return tiles


def main():
    tiles = read_tiles()
    process_crew_list(tiles)


if __name__ == "__main__":
    sys.exit(main())
