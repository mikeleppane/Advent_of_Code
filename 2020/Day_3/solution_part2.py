#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum

import sys
from math import prod
from typing import List, Literal, Set

INPUT_FILE = "input.txt"


class MapTypes(Enum):
    TREE = "tree"
    OPEN_SQUARE = "open_square"


@dataclass(frozen=True, eq=True)
class Coordinate:
    x: int
    y: int
    map_type: Literal[MapTypes.TREE, MapTypes.OPEN_SQUARE]


@dataclass
class Map:
    coordinates: List[Coordinate]

    def resize_by_one(self) -> None:
        last_column_index = self.coordinates[-1].x
        coordinates = self.coordinates[:]
        for coordinate in coordinates:
            self.coordinates.append(
                Coordinate(
                    x=coordinate.x + last_column_index + 1,
                    y=coordinate.y,
                    map_type=coordinate.map_type,
                )
            )


def generate_map() -> Map:
    coordinates = list()
    with open(INPUT_FILE, "r") as f_handle:
        for row, line in enumerate(f_handle):
            if line:
                for column, char in enumerate(list(line.rstrip())):
                    coordinates.append(
                        Coordinate(
                            x=column,
                            y=row,
                            map_type=MapTypes.OPEN_SQUARE
                            if char == "."
                            else MapTypes.TREE,
                        )
                    )

    return Map(coordinates)


def find_trees_during_travel(_map: Map) -> List[int]:
    slopes = [[7, 1], [1, 1], [3, 1], [5, 1], [1, 2]]
    encountered_trees = []
    for slope in slopes:
        trees = 0
        position = [0, 0]
        unordered_coordinates = set(_map.coordinates)
        while True:
            position[0] += slope[0]
            position[1] += slope[1]
            if position[0] > _map.coordinates[-1].x:
                _map.resize_by_one()
                unordered_coordinates = set(_map.coordinates)
            if position[1] > _map.coordinates[-1].y:
                break
            coordinate = Coordinate(
                x=position[0], y=position[1], map_type=MapTypes.TREE
            )
            if coordinate in unordered_coordinates:
                trees += 1
                continue
        encountered_trees.append(trees)
    return encountered_trees


def main():
    _map = generate_map()
    trees = find_trees_during_travel(_map)
    print(prod(trees))


if __name__ == "__main__":
    sys.exit(main())
