#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import numpy as np
import re
import sys
from itertools import repeat
from math import prod
from pprint import PrettyPrinter
from typing import List

INPUT_FILE = "input.txt"
TILE_SIZE = 10


@dataclass
class Tile:
    id: int
    data: np.array


def has_same_border(tile_1: np.array, tile_2: np.array):
    return (
        np.array_equal(tile_1[:, -1], tile_2[:, 0])
        or np.array_equal(tile_1[:, 0], tile_2[:, -1])
        or np.array_equal(tile_1[-1, :], tile_2[0, :])
        or np.array_equal(tile_1[0, :], tile_2[-1, :])
    )


def reorganize_tiles(tiles: List[Tile]):
    corner_tiles = {}
    for tile in tiles:
        current_tile_data: np.array = np.array(tile.data)
        select_new_tile = False
        for _ in range(0, 2):
            current_tile_data = np.flipud(current_tile_data)
            for _ in range(0, 2):
                current_tile_data = np.fliplr(current_tile_data)
                for rotation in repeat(-1, 4):
                    current_tile_data = np.rot90(current_tile_data, rotation)
                    same_borders = set()
                    for other_tile in tiles:
                        other_tile_data = np.array(other_tile.data)
                        if other_tile.id != tile.id:
                            for _ in range(0, 2):
                                other_tile_data = np.flipud(other_tile_data)
                                for _ in range(0, 2):
                                    other_tile_data = np.fliplr(other_tile_data)
                                    for rot in repeat(-1, 4):
                                        other_tile_data = np.rot90(other_tile_data, rot)
                                        if has_same_border(
                                            current_tile_data, other_tile_data
                                        ):
                                            same_borders.add(other_tile.id)
                    if len(same_borders) == 2:
                        print(same_borders)
                        corner_tiles[tile.id] = set(same_borders)
                        print(corner_tiles)
                        select_new_tile = True
                        break
                if select_new_tile:
                    break
            if select_new_tile:
                break

    print(prod(corner_tiles.keys()))


def read_tiles() -> List[Tile]:
    tiles = []
    id_regex = re.compile(r"Tile\s(\d+)\:")
    with open(INPUT_FILE, "r") as f_handle:
        tile_sections = f_handle.read().split("\n\n")
        for tile_section in tile_sections:
            tile_section = tile_section.split("\n")
            match_id = id_regex.match(tile_section[0])
            if match_id:
                tile_id = int(match_id.groups()[0])
            else:
                raise ValueError(
                    f"Trying to parse incorrect tile id: {tile_section[0]}"
                )
            data = np.empty((TILE_SIZE, TILE_SIZE), dtype=str)
            for index, tile_row in enumerate(tile_section[1:]):
                data[index, :] = list(tile_row)
            tiles.append(Tile(id=tile_id, data=data))

    return tiles


def main():
    pp = PrettyPrinter(indent=4)
    tiles = read_tiles()
    # pp.pprint(np.flipud(np.flipud(tiles[0].data)))
    reorganize_tiles(tiles)


if __name__ == "__main__":
    sys.exit(main())
