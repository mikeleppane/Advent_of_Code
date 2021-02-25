#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass

import numpy as np
import re
import sys
from itertools import repeat
from typing import List, Tuple, Optional

INPUT_FILE = "input.txt"
TILE_SIZE = 10
CAMERA_ARRAY_SIZE = 12
TOP, RIGHT, BOTTOM, LEFT = (0, 1, 2, 3)


@dataclass
class Tile:
    id: int
    data: np.array


def check_same_border(tile_1: np.array, tile_2: np.array) -> Tuple[bool, Optional[int]]:
    if np.array_equal(tile_1[:, -1], tile_2[:, 0]):
        return True, RIGHT
    elif np.array_equal(tile_1[:, 0], tile_2[:, -1]):
        return True, LEFT
    elif np.array_equal(tile_1[-1, :], tile_2[0, :]):
        return True, BOTTOM
    elif np.array_equal(tile_1[0, :], tile_2[-1, :]):
        return True, TOP
    else:
        return False, None


visited_ids = deque()
new_array = list()


def assemble(current_tile_data: np.array, tiles: List[Tile]):
    if len(new_array) == 144:
        return True
    found = False
    for tile in tiles:
        tile_data = tile.data
        if tile.id not in visited_ids:
            for _ in range(0, 2):
                tile_data = np.flipud(tile_data)
                for _ in range(0, 2):
                    tile_data = np.fliplr(tile_data)
                    for rot in repeat(-1, 4):
                        tile_data = np.rot90(tile_data, rot)
                        if len(new_array) % 12 != 0:
                            has_same_border, border = check_same_border(
                                current_tile_data, tile_data
                            )
                            if has_same_border and border == RIGHT:
                                found = True
                                visited_ids.append(tile.id)
                                new_array.append(tile_data)
                                if assemble(tile_data, tiles):
                                    return True
                        else:
                            has_same_border, border = check_same_border(
                                new_array[-12], tile_data
                            )
                            if has_same_border and border == BOTTOM:
                                found = True
                                visited_ids.append(tile.id)
                                new_array.append(tile_data)
                                if assemble(tile_data, tiles):
                                    return True

    if not found:
        if len(new_array) > 1:
            visited_ids.pop()
            del new_array[-1]
            return False
    else:
        return True


def assemble_array(tiles: List[Tile]):
    for tile in tiles:
        if tile.id in (2797, 3167, 3593, 3517):
            current_tile_data: np.array = np.array(tile.data)
            visited_ids.clear()
            visited_ids.append(tile.id)
            new_array.clear()
            new_array.append(0)
            for _ in range(0, 2):
                current_tile_data = np.flipud(current_tile_data)
                for _ in range(0, 2):
                    current_tile_data = np.fliplr(current_tile_data)
                    for rotation in repeat(-1, 4):
                        current_tile_data = np.rot90(current_tile_data, rotation)
                        new_array[0] = current_tile_data
                        valid = assemble(current_tile_data, tiles)
                        if len(new_array) == 144:
                            return
                        if not valid:
                            continue


def find_monsters():
    new_tiles = []
    data = np.empty((96, 96), dtype=str)
    for tile in new_array:
        new_tiles.append(tile[1:-1, 1:-1])
    for index, i in enumerate(range(0, 144, 12)):
        for j in range(8):
            sea = ""
            for k in range(12):
                sea += (
                    new_tiles[i + k][j, :].tobytes().decode("utf-8").replace("\x00", "")
                )
            for ii, c in enumerate(list(sea)):
                data[index * 8 + j, ii] = c
    first_line = re.compile(r"(?=[#.]{18}#[#.]{1})")
    second_line = re.compile(r"#[.#]{4}##[.#]{4}##[.#]{4}###")
    thrid_line = re.compile(r"[.#]{1}#[.#]{2}#[.#]{2}#[.#]{2}#[.#]{2}#[.#]{2}#[.#]{3}")
    max_roughness = float("inf")
    for _ in range(0, 2):
        other_tile_data = np.flipud(data)
        for _ in range(0, 2):
            other_tile_data = np.fliplr(other_tile_data)
            for rot in repeat(-1, 4):
                other_tile_data = np.rot90(other_tile_data, rot)
                sea = ""
                count = 0
                for i in range(93):
                    for match in first_line.finditer(other_tile_data[i, :]
                        .tobytes()
                        .decode("utf-8")
                        .replace("\x00", "")):
                        if match:
                            m2 = second_line.match(other_tile_data[i+1, :]
                                                  .tobytes()
                                                  .decode("utf-8")
                                                  .replace("\x00", ""), match.start())
                            m3 = thrid_line.match(other_tile_data[i+2, :]
                                                  .tobytes()
                                                  .decode("utf-8")
                                                  .replace("\x00", ""), match.start())
                            if m2 and m3:
                                count += 1
                if count > 0:
                    print(count)
                    """
                    sea += (
                        other_tile_data[i, :]
                        .tobytes()
                        .decode("utf-8")
                        .replace("\x00", "")
                    )
                    """
                #print(count)
                #print(len(tr.findall(sea)))
                #print(sea.count("#"))
                #max_roughness = min(max_roughness, sea.count('#') - len(tr.findall(sea)) * 15)
    #print(max_roughness)


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
    tiles = read_tiles()
    assemble_array(tiles)
    find_monsters()


if __name__ == "__main__":
    sys.exit(main())
