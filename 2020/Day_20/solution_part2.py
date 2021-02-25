#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import numpy as np
import re
import sys
from collections import defaultdict
from itertools import repeat
from math import prod
from pprint import PrettyPrinter
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


def check_tile_validity(tile_data, id,  tiles: List[Tile]):
    valid_corner_border_1 = {RIGHT, BOTTOM, LEFT}
    current_tile_data: np.array = np.array(tile_data)
    same_borders = defaultdict(int)
    found = False
    for other_tile in tiles:
        other_tile_data = np.array(other_tile.data)
        if other_tile.id != id:
            for _ in range(0, 2):
                other_tile_data = np.flipud(other_tile_data)
                for _ in range(0, 2):
                    other_tile_data = np.fliplr(other_tile_data)
                    for rot in repeat(-1, 4):
                        other_tile_data = np.rot90(other_tile_data, rot)
                        has_same_border, border = check_same_border(
                            current_tile_data, other_tile_data
                        )
                        if has_same_border and border == TOP:
                            return False
                        if has_same_border:
                            same_borders[other_tile.id] = border
                            if len(same_borders) == 3:
                                found = True
                                break
        if len(same_borders) == 3 and set(same_borders.values()) == valid_corner_border_1 and same_borders[1951] == LEFT:
            return True
    return False


def get_first_corner_tile(tiles: List[Tile]):
    valid_corner_border = {RIGHT, BOTTOM}
    #for tile in tiles[1:2]:
    while True:
        current_tile_data: np.array = np.array(tiles[1].data)
        for _ in range(0, 2):
            current_tile_data = np.flipud(current_tile_data)
            for _ in range(0, 2):
                current_tile_data = np.fliplr(current_tile_data)
                for rotation in repeat(-1, 4):
                    current_tile_data = np.rot90(current_tile_data, rotation)
                    same_borders = defaultdict(list)

                    found = False
                    for other_tile in (tiles[-2], tiles[-2]):
                        other_tile_data = other_tile.data
                        if other_tile.id != tiles[1].id:
                            for _ in range(0, 2):
                                other_tile_data = np.flipud(other_tile_data)
                                for _ in range(0, 2):
                                    other_tile_data = np.fliplr(other_tile_data)
                                    for rot in repeat(-1, 4):
                                        other_tile_data = np.rot90(other_tile_data, rot)
                                        has_same_border, border = check_same_border(
                                            current_tile_data, other_tile_data
                                        )
                                        if has_same_border and check_tile_validity(other_tile_data, other_tile.id, tiles):
                                            same_borders[other_tile.id] = border # [other_tile_data, border]
                                            #print(current_tile_data)
                                            #print("\n")
                                            #print(same_borders)
                                            return current_tile_data
                                if found:
                                    break
                    #print(same_borders)
                    borbers = list()
                    """
                    for data, border in same_borders.values():
                        borbers.append(border)
                    """
                    """
                    if len(same_borders) == 2 and set(same_borders.values()) == valid_corner_border: #and same_borders[1951] == LEFT:
                        gg = list()
                        for _id, data in same_borders.items():
                            if data[1] == RIGHT:
                                gg.append(check_tile_validity(data[0], _id, tiles, tiles[1]))
                                print(same_borders)
                        if all(gg):
                            print(same_borders)
                            print("\n")
                            print(current_tile_data)
                            return dict({tiles[1].id: same_borders.values(), "other_tiles": 33})
                    """


def assembly(first_data, tiles: List[Tile]):
    t = list()
    t.append(first_data)
    ids = list()
    ids.append(1951)
    found = False
    for i in range(3):
        for j in range(3):
            if j == 0 and i == 0:
                continue
            for index, tile in enumerate(tiles):
                found = False
                if (j == 0 and tile.id == ids[-3]) or tile.id == ids[-1]:
                    continue
                if tile.id not in ids:
                    for _ in range(0, 2):
                        other_tile_data = np.flipud(tile.data)
                        for _ in range(0, 2):
                            other_tile_data = np.fliplr(other_tile_data)
                            for rot in repeat(-1, 4):
                                other_tile_data = np.rot90(other_tile_data, rot)
                                if j == 0:
                                    has_same_border, border = check_same_border(
                                        t[-3], other_tile_data
                                    )
                                    if has_same_border and border == BOTTOM:
                                        #print(other_tile_data)
                                        #print(tile.id)
                                        t.append(other_tile_data)
                                        ids.append(tile.id)
                                        found = True
                                        break
                                else:
                                    has_same_border, border = check_same_border(
                                        t[-1], other_tile_data
                                    )
                                    if has_same_border and border == RIGHT:
                                        #print(other_tile_data)
                                        #print(tile.id)
                                        t.append(other_tile_data)
                                        ids.append(tile.id)
                                        found = True
                                        break
                            if found:
                                break
                        if found:
                            break

    g = []
    data = np.empty((24,24), dtype=str)
    for tile in t:
        g.append(tile[1:-1, 1:-1])
    for index, i in enumerate(range(0,9,3)):
        for j in range(8):
            sea = ""
            for k in range(3):
                sea += g[i + k][j,:].tobytes().decode("utf-8").replace('\x00','')
            #print(len(sea))
            #print(index)
            for ii, c in enumerate(list(sea)):
                data[index*8 + j, ii] = c
    #tr = re.compile(r"([.#]*[#]{1}[.#]*[#]{1}[.#]{4}[#]{2}[.#]{4}[#]{2}[.#]{4}[#]{3}[.#]*[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1})*")
    tr = re.compile(r"[#]{1}[.#]{1,24}#[.#]{4}##[.#]{4}##[.#]{4}###[.#]{1,24}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}[.#]{2}[#]{1}")
    for _ in range(0, 2):
        other_tile_data = np.flipud(data)
        for _ in range(0, 2):
            other_tile_data = np.fliplr(other_tile_data)
            for rot in repeat(-1, 4):
                other_tile_data = np.rot90(other_tile_data, rot)
                sea = ""
                for i in range(24):
                    sea += other_tile_data[i,:].tobytes().decode("utf-8").replace('\x00', '')
                #print(sea.count('#') - )
                print(len(tr.findall(sea)))
                #print(len(tr.match(sea).groups()))



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
    d = get_first_corner_tile(tiles)
    assembly(d, tiles)

if __name__ == "__main__":
    sys.exit(main())
