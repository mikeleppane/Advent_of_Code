#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from enum import IntEnum, Enum

import sys
from collections import Counter
from itertools import product
from typing import NamedTuple, Dict, Tuple, Union
from copy import deepcopy
from pprint import PrettyPrinter

INPUT_FILE = "input.txt"

ELF, GOBLIN, WALL, OPEN_CAVERN = ("elf", "goblin", "#", ".")

pp = PrettyPrinter(indent=4)


class AreaType(Enum):
    WALL = "#"
    OPEN_CAVERN = "."


class Coordinate(NamedTuple):
    x: int
    y: int


class Area(NamedTuple):
    type: str = ""


@dataclass
class Elf:
    name: str = ELF
    is_attacking: bool = False
    attack_power: int = 3
    hit_points: int = 200


@dataclass
class Goblin:
    name: str = GOBLIN
    is_attacking: bool = False
    attack_power: int = 3
    hit_points: int = 200


visited_points = set()
travel_distances = {}  # Counter()
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def start_combat(
    area: Dict[Coordinate, Area], units: Dict[Coordinate, Union[Elf, Goblin]]
):
    round = 0
    while True:
        for starting_coordinate, unit in sorted(
            units.items(), key=lambda item: (item[0][1], item[0][0])
        ):
            print(round)
            new_places = {}
            if isinstance(unit, Goblin):
                targets = {
                    coordinate: unit2
                    for coordinate, unit2 in units.items()
                    if isinstance(unit2, Elf) and unit2.hit_points > 0
                }
            else:
                targets = {
                    coordinate: unit2
                    for coordinate, unit2 in units.items()
                    if isinstance(unit2, Goblin) and unit2.hit_points > 0
                }
            if not targets:
                print(round)
                for key, value in units.items():
                    if unit.name == value.name:
                        print(value.hit_points)
                return
            in_range_enemies = []
            for end_coordinate, target in targets.items():
                in_range_points = []
                for direction in directions:
                    next_point = tuple(sum(x) for x in zip(end_coordinate, direction))
                    if next_point in area:
                        in_range_points.append(next_point)
                if in_range_points and starting_coordinate in in_range_points:
                    in_range_enemies.append((end_coordinate, target))
            if in_range_enemies:
                unit.is_attacking = True
            else:
                unit.is_attacking = False

            travel_distances.clear()
            rr = None
            if not unit.is_attacking:
                for end_coordinate, elf in targets.items():
                    in_range_poins = []
                    for direction in directions:
                        next_point = tuple(
                            sum(x) for x in zip(end_coordinate, direction)
                        )
                        if next_point in area and area[next_point].type == OPEN_CAVERN:
                            in_range_poins.append(next_point)
                    if in_range_poins and starting_coordinate not in in_range_poins:
                        for in_range_point in in_range_poins:
                            for direction in directions:
                                visited_points.clear()
                                seen.clear()
                                next_dir = tuple(
                                    sum(x) for x in zip(starting_coordinate, direction)
                                )
                                if (
                                    next_dir in area
                                    and area[next_dir].type == OPEN_CAVERN
                                ):
                                    visited_points.add(starting_coordinate)
                                    visited_points.add(next_dir)
                                    #print(starting_coordinate, next_dir, in_range_point, area[in_range_point])
                                    found = walk(next_dir, in_range_point, area)
                                    if found:
                                        travel_distances[
                                            (next_dir, in_range_point)
                                        ] = len(visited_points) - 1
                if travel_distances:
                    min_distance = min(travel_distances.values())
                    possible_distances = {
                        coordinates: distance
                        for coordinates, distance in travel_distances.items()
                        if distance == min_distance
                    }
                    new_point = sorted(
                        possible_distances.items(),
                        key=lambda item: (item[0][0][1], item[0][0][0]),
                    )[0][0][0]
                    if (new_point, starting_coordinate) not in new_places:
                        if min_distance == 1:
                            unit.frozen = True
                        new_places[(new_point, starting_coordinate)] = unit

                for places, unit in new_places.items():
                    rr = places[0]
                    units[places[0]] = unit
                    del units[starting_coordinate]
                    area[places[0]] = Area(type=unit.name)
                    if area[starting_coordinate].type != unit.name:
                        area[starting_coordinate] = Area(type=OPEN_CAVERN)
            if isinstance(unit, Goblin):
                targets = {
                    coordinate: unit2
                    for coordinate, unit2 in units.items()
                    if isinstance(unit2, Elf) and unit2.hit_points > 0
                }
            else:
                targets = {
                    coordinate: unit2
                    for coordinate, unit2 in units.items()
                    if isinstance(unit2, Goblin) and unit2.hit_points > 0
                }
            in_range_enemies = []
            ee = starting_coordinate
            if rr:
                ee = rr
            for end_coordinate, target in targets.items():
                in_range_points = []
                for direction in directions:
                    next_point = tuple(sum(x) for x in zip(end_coordinate, direction))
                    if next_point in area:
                        in_range_points.append(next_point)
                if in_range_points and ee in in_range_points:
                    in_range_enemies.append((end_coordinate, target))
            if in_range_enemies:
                lowest_hit_point = min(e.hit_points for c, e in in_range_enemies)
                in_range_enemies = [
                    (c, e)
                    for c, e in in_range_enemies
                    if e.hit_points == lowest_hit_point
                ]
                target_coordinate, enemy = sorted(
                    in_range_enemies, key=lambda x: (x[0][1], x[0][0])
                )[0]
                enemy.hit_points -= 3
                if enemy.hit_points < 0:
                    enemy.hit_points = 0
                    area[target_coordinate] = Area(type=OPEN_CAVERN)
        units = {
            starting_coordinate: unit
            for starting_coordinate, unit in units.items()
            if unit.hit_points > 0
        }
        #if round == 2:
        #    print()
        #    pp.pprint(units)
        #    return
        round += 1


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

seen = set()

def walk(start: Coordinate, end: Coordinate, area: Dict[Coordinate, Area]):
    if start == end:
        return True
    new_dirs = {}
    for direction in directions:
        next_dir = tuple(sum(x) for x in zip(start, direction))
        if (
            next_dir in area
            and area[next_dir].type != WALL
            and next_dir not in visited_points and next_dir not in seen
        ):
            new_dirs[next_dir] = manhattan(next_dir, end)
    if not new_dirs:
        seen.add(start)
        #visited_points.remove(start)
        return False
    new_dirs = dict(sorted(new_dirs.items(), key=lambda item: item[1]))
    for next_dir in new_dirs.keys():
        visited_points.add(next_dir)
        found = walk(next_dir, end, area)
        if found:
            return True
        else:
            seen.add(next_dir)
            #visited_points.remove(next_dir)
    return False


def scan_area() -> Tuple:
    area = {}
    units = {}
    with open(INPUT_FILE, "r") as f_handle:
        for y, line in enumerate(f_handle):
            line = line.rstrip("\n")
            if line:
                for x, area_type in enumerate(line):
                    if area_type in ("G", "E"):
                        if area_type == "G":
                            units[Coordinate(x=x, y=y)] = Goblin()
                        else:
                            units[Coordinate(x=x, y=y)] = Elf()
                    area[Coordinate(x=x, y=y)] = Area(type=area_type)

    return area, units


def main():
    area, units = scan_area()
    #walk(start=(11,11),end=(27,18),area=area)
    start_combat(area, units)


if __name__ == "__main__":
    sys.exit(main())
