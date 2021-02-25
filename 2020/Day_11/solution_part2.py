#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import sys
from typing import NamedTuple, Dict

INPUT_FILE = "input.txt"


class Layout:
    x_size = 0
    y_size = 0


class MapTypes(Enum):
    FLOOR = "."
    OCCUPIED = "#"
    EMPTY = "L"


class Coordinate(NamedTuple):
    x: int
    y: int


@dataclass
class Map:
    coordinates: Dict[Coordinate, MapTypes]


def generate_map() -> Map:
    coordinates = dict()
    with open(INPUT_FILE, "r") as f_handle:
        for row, line in enumerate(f_handle):
            if line:
                for column, char in enumerate(list(line.rstrip())):
                    map_type = MapTypes.FLOOR if char == "." else MapTypes.EMPTY
                    coordinates[Coordinate(x=column, y=row)] = map_type

    return Map(coordinates)


def get_direction_indexes(direction, x, y):
    if direction == 1 and y > 0:
        for y_step in range(y - 1, -1, -1):
            yield x, y_step
    elif direction == 2 and x < Layout.x_size and y > 0:
        for x_step, y_step in zip(
            range(x + 1, Layout.x_size + 1), range(y - 1, -1, -1)
        ):
            yield x_step, y_step
    elif direction == 3 and x < Layout.x_size:
        for x_step in range(x + 1, Layout.x_size + 1):
            yield x_step, y
    elif direction == 4 and x < Layout.x_size and y < Layout.y_size:
        for x_step, y_step in zip(
            range(x + 1, Layout.x_size + 1), range(y + 1, Layout.y_size + 1)
        ):
            yield x_step, y_step
    elif direction == 5 and y < Layout.y_size:
        for y_step in range(y + 1, Layout.y_size + 1):
            yield x, y_step
    elif direction == 6 and x > 0 and y < Layout.y_size:
        for x_step, y_step in zip(
            range(x - 1, -1, -1), range(y + 1, Layout.y_size + 1)
        ):
            yield x_step, y_step
    elif direction == 7 and x > 0:
        for x_step in range(x - 1, -1, -1):
            yield x_step, y
    elif direction == 8 and x > 0 and y > 0:
        for x_step, y_step in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
            yield x_step, y_step


def should_become_occupied(coordinate: Coordinate, _map: Map) -> bool:
    for index in range(1, 9):
        for row, column in get_direction_indexes(index, coordinate.x, coordinate.y):
            if (row, column) in _map.coordinates and _map.coordinates[
                Coordinate(row, column)
            ] == MapTypes.OCCUPIED:
                return False
            elif (row, column) in _map.coordinates and _map.coordinates[
                Coordinate(row, column)
            ] == MapTypes.EMPTY:
                break
    return True


def should_become_empty(coordinate: Coordinate, _map: Map) -> bool:
    number_of_adjacent_occupied_seats = 0
    for index in range(1, 9):
        for row, column in get_direction_indexes(index, coordinate.x, coordinate.y):
            if (row, column) in _map.coordinates and _map.coordinates[
                Coordinate(row, column)
            ] == MapTypes.OCCUPIED:
                number_of_adjacent_occupied_seats += 1
                break
            elif (row, column) in _map.coordinates and _map.coordinates[
                Coordinate(row, column)
            ] == MapTypes.EMPTY:
                break
        if number_of_adjacent_occupied_seats >= 5:
            return True
    return False


def simulate_people_flow(_map: Map):
    while True:
        prev_map = Map(deepcopy(_map.coordinates))
        for coordinate, map_type in prev_map.coordinates.items():
            if map_type == MapTypes.EMPTY:
                if should_become_occupied(coordinate, prev_map):
                    _map.coordinates[
                        Coordinate(coordinate.x, coordinate.y)
                    ] = MapTypes.OCCUPIED
            elif map_type == MapTypes.OCCUPIED:
                if should_become_empty(coordinate, prev_map):
                    _map.coordinates[
                        Coordinate(coordinate.x, coordinate.y)
                    ] = MapTypes.EMPTY
        if _map.coordinates == prev_map.coordinates:
            print(
                sum(
                    [
                        1
                        for map_type in _map.coordinates.values()
                        if map_type == MapTypes.OCCUPIED
                    ]
                )
            )
            break


def main():
    _map = generate_map()
    x, y = sorted(_map.coordinates)[-1]
    Layout.x_size = x
    Layout.y_size = y
    simulate_people_flow(_map)


if __name__ == "__main__":
    sys.exit(main())
