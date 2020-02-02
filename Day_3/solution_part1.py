#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import sys
from typing import NamedTuple


INPUT_FILE = "input.txt"

pp = pprint.PrettyPrinter(indent=4)


class Point(NamedTuple):
    x: int
    y: int


class Movement(NamedTuple):
    direction: str
    distance: int


class Wire:
    def __init__(self, movements):
        self.movements = self._process_movements(list(movements))
        self.locations = [Point(1, 1)]

    def process_wire_path(self):
        for movement in self.movements:
            last_point = self.locations[-1]
            if movement.direction == Grid.RIGHT:
                for index in range(1, movement.distance + 1):
                    self.locations.append(Point(last_point.x + index, last_point.y))
            if movement.direction == Grid.LEFT:
                for index in range(1, movement.distance + 1):
                    self.locations.append(Point(last_point.x - index, last_point.y))
            if movement.direction == Grid.UP:
                for index in range(1, movement.distance + 1):
                    self.locations.append(Point(last_point.x, last_point.y + index))
            if movement.direction == Grid.DOWN:
                for index in range(1, movement.distance + 1):
                    self.locations.append(Point(last_point.x, last_point.y - index))

    @staticmethod
    def _process_movements(movements):
        new_movements = []
        for movement in movements:
            new_movements.append(Movement(movement[0], int(movement[1:])))
        return new_movements


class Grid:
    UP, DOWN, LEFT, RIGHT = ("U", "D", "L", "R")
    central_port = Point(1, 1)
    wires = []

    @staticmethod
    def process_wire_movements_points():
        for wire in Grid.wires:
            wire.process_wire_path()


def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def read_input():
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle.readlines():
            Grid.wires.append(Wire(line.rstrip().split(",")))


def calculate_crossing_points():
    path_1 = set(Grid.wires[0].locations)
    path_1.remove(Point(1, 1))
    path_2 = set(Grid.wires[1].locations)
    path_2.remove(Point(1, 1))
    return path_1.intersection(path_2)


def find_minimun_distance():
    intersections = calculate_crossing_points()
    min_distance = float("inf")
    for intersection in intersections:
        distance = manhattan_distance([intersection.x, 1], [1, intersection.y])
        min_distance = min(min_distance, distance)
    return min_distance


def main():
    read_input()
    Grid.process_wire_movements_points()
    print(find_minimun_distance())


if __name__ == "__main__":
    sys.exit(main())
