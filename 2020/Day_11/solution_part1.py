#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import sys
from typing import NamedTuple, Dict

INPUT_FILE = "input.txt"


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
                    map_type = MapTypes.FLOOR if char == '.' else MapTypes.EMPTY
                    coordinates[Coordinate(x=column, y=row)] = map_type

    return Map(coordinates)


def get_neighbour_indexes(row, column):
    return [
        (row - 1, column - 1),
        (row - 1, column),
        (row - 1, column + 1),
        (row, column - 1),
        (row, column + 1),
        (row + 1, column - 1),
        (row + 1, column),
        (row + 1, column + 1),
    ]


def should_become_occupied(coordinate: Coordinate, _map: Map) -> bool:
    adjacent_indexes = get_neighbour_indexes(coordinate.x, coordinate.y)
    for row, column in adjacent_indexes:
        if (row, column) in _map.coordinates and _map.coordinates[
            Coordinate(row, column)
        ] == MapTypes.OCCUPIED:
            return False
    return True


def should_become_empty(coordinate: Coordinate, _map: Map) -> bool:
    adjacent_indexes = get_neighbour_indexes(coordinate.x, coordinate.y)
    number_of_adjacent_occupied_seats = 0
    for row, column in adjacent_indexes:
        if (row, column) in _map.coordinates and _map.coordinates[
            Coordinate(row, column)
        ] == MapTypes.OCCUPIED:
            number_of_adjacent_occupied_seats += 1
    if number_of_adjacent_occupied_seats >= 4:
        return True
    return False


def simulate_people_flow(_map: Map):
    while True:
        prev_map = Map(deepcopy(_map.coordinates))
        for coordinate, map_type in prev_map.coordinates.items():
            if map_type == MapTypes.EMPTY:
                if should_become_occupied(coordinate, prev_map):
                    _map.coordinates[Coordinate(coordinate.x, coordinate.y)] = MapTypes.OCCUPIED
            elif map_type == MapTypes.OCCUPIED:
                if should_become_empty(coordinate, prev_map):
                    _map.coordinates[Coordinate(coordinate.x, coordinate.y)] = MapTypes.EMPTY
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
    simulate_people_flow(_map)


if __name__ == "__main__":
    sys.exit(main())
