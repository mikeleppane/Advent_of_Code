#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from itertools import permutations
from operator import add
import sys
from typing import NamedTuple, Dict
from pprint import PrettyPrinter

INPUT_FILE = "input.txt"
BOOT_UP_CYCLES = 6


class State(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int
    w: int


@dataclass
class PocketDimension:
    cubes: Dict[Coordinate, State]


ADJACENT_INDICES_4D = set()


def read_initial_state() -> PocketDimension:
    cube_states = dict()
    with open(INPUT_FILE, "r") as f_handle:
        for row, line in enumerate(f_handle):
            line = line.rstrip()
            if line:
                for column, char in enumerate(list(line)):
                    cube_state = State.INACTIVE if char == "." else State.ACTIVE
                    cube_states[Coordinate(x=column, y=row, z=0, w=0)] = cube_state

    return PocketDimension(cubes=cube_states)


def get_cube_neighbor_indexes(x, y, z, w):
    indexes = list()
    for hyber_cube_index in ADJACENT_INDICES_4D:
        indexes.append(tuple(map(add, (x, y, z, w), hyber_cube_index)))
    return indexes


def boot_up_energy_source(pocket_dimension: PocketDimension):
    pp = PrettyPrinter(indent=4)
    for _ in range(6):
        prev_pocket_dim = PocketDimension(deepcopy(pocket_dimension.cubes))
        for coordinate, state in prev_pocket_dim.cubes.items():
            adjacent_indexes = get_cube_neighbor_indexes(
                coordinate.x, coordinate.y, coordinate.z, coordinate.w
            )
            if state == State.ACTIVE:
                number_of_active_adjacent_cubes = 0
                for x, y, z, w in adjacent_indexes:
                    if (
                        prev_pocket_dim.cubes.get(Coordinate(x, y, z, w))
                        == State.ACTIVE
                    ):
                        number_of_active_adjacent_cubes += 1
                    elif Coordinate(x, y, z, w) not in prev_pocket_dim.cubes:
                        if (
                            sum(
                                (
                                    1
                                    for x_2, y_2, z_2, w_2 in get_cube_neighbor_indexes(
                                        x, y, z, w
                                    )
                                    if prev_pocket_dim.cubes.get(
                                        Coordinate(x_2, y_2, z_2, w_2)
                                    )
                                    == State.ACTIVE
                                )
                            )
                            == 3
                        ):
                            pocket_dimension.cubes[
                                Coordinate(x, y, z, w)
                            ] = State.ACTIVE
                if number_of_active_adjacent_cubes not in (2, 3):
                    pocket_dimension.cubes[
                        Coordinate(
                            coordinate.x, coordinate.y, coordinate.z, coordinate.w
                        )
                    ] = State.INACTIVE
            elif state == State.INACTIVE:
                number_of_active_adjacent_cubes = 0
                for x, y, z, w in adjacent_indexes:
                    if (x, y, z, w) in prev_pocket_dim.cubes and prev_pocket_dim.cubes[
                        Coordinate(x, y, z, w)
                    ] == State.ACTIVE:
                        number_of_active_adjacent_cubes += 1
                    elif Coordinate(x, y, z, w) not in prev_pocket_dim.cubes:
                        adjacent_indexes_2 = get_cube_neighbor_indexes(x, y, z, w)
                        number_of_active_adjacent_cubes_2 = 0
                        for x_2, y_2, z_2, w_2 in adjacent_indexes_2:
                            if (
                                x_2,
                                y_2,
                                z_2,
                                w_2,
                            ) in prev_pocket_dim.cubes and prev_pocket_dim.cubes[
                                Coordinate(x_2, y_2, z_2, w_2)
                            ] == State.ACTIVE:
                                number_of_active_adjacent_cubes_2 += 1
                        if number_of_active_adjacent_cubes_2 == 3:
                            pocket_dimension.cubes[
                                Coordinate(x, y, z, w)
                            ] = State.ACTIVE
                if number_of_active_adjacent_cubes == 3:
                    pocket_dimension.cubes[
                        Coordinate(
                            coordinate.x, coordinate.y, coordinate.z, coordinate.w
                        )
                    ] = State.ACTIVE
    print(
        sum([1 for state in pocket_dimension.cubes.values() if state == State.ACTIVE])
    )


def set_4d_adjacent_indices():
    for index_4d in set(permutations([-1, -1, -1, -1, 1, 1, 1, 1, 0, 0, 0], 4)):
        ADJACENT_INDICES_4D.add(index_4d)


def main():
    set_4d_adjacent_indices()
    pocket_dims = read_initial_state()
    boot_up_energy_source(pocket_dims)


if __name__ == "__main__":
    sys.exit(main())
