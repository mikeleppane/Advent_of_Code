#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum

from itertools import cycle
import numpy as np
import re
import sys
from typing import List

INPUT_FILE = "input.txt"


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
    LEFT = "L"
    RIGHT = "R"
    FORWARD = "F"


@dataclass(eq=True)
class CurrentPosition:
    previous_direction: Direction = Direction.EAST
    direction: Direction = Direction.EAST
    NS: Direction = Direction.NORTH
    NS_value: int = 0
    EW: Direction = Direction.EAST
    EW_value: int = 0


@dataclass(eq=True)
class WayPoint:
    previous_direction: Direction = Direction.EAST
    direction: Direction = Direction.EAST
    NS: Direction = Direction.NORTH
    NS_value: int = 1
    EW: Direction = Direction.EAST
    EW_value: int = 10


@dataclass(frozen=True, eq=True)
class NavInstruction:
    action: Direction
    value: int


def rotate(p, degrees=0):
    origin = (0, 0)
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T - o.T) + o.T).T)


def get_new_direction(waypoint: WayPoint, nav_instruction: NavInstruction):
    x = 0
    y = 0
    if waypoint.NS == Direction.NORTH:
        y = waypoint.NS_value
    elif waypoint.NS == Direction.SOUTH:
        y = -1 * waypoint.NS_value
    if waypoint.EW == Direction.EAST:
        x = waypoint.EW_value
    elif waypoint.EW == Direction.WEST:
        x = -1 * waypoint.EW_value
    if nav_instruction.action == Direction.LEFT:
        new_values = rotate((x, y), degrees=nav_instruction.value)
    elif nav_instruction.action == Direction.RIGHT:
        new_values = rotate((x, y), degrees=-1 * nav_instruction.value)
    x_new, y_new = new_values
    print(new_values)
    waypoint.EW_value = abs(round(x_new))
    if x_new < 0:
        waypoint.EW = Direction.WEST
    else:
        waypoint.EW = Direction.EAST
    waypoint.NS_value = abs(round(y_new))
    if y_new < 0:
        waypoint.NS = Direction.SOUTH
    else:
        waypoint.NS = Direction.NORTH

    """
    directions = {
        0: Direction.NORTH,
        1: Direction.EAST,
        2: Direction.SOUTH,
        3: Direction.WEST,
    }
    current_direction_value = 0
    for key, value in directions.items():
        if value == current_direction:
            current_direction_value = key
            break
    if nav_instruction.value == 90 and nav_instruction.action == Direction.RIGHT:
        new_value = current_direction_value + 1
        if new_value > 3:
            new_value = 0
        return directions[new_value]
    if nav_instruction.value == 90 and nav_instruction.action == Direction.LEFT:
        new_value = current_direction_value - 1
        if new_value < 0:
            new_value = 3
        return directions[new_value]
    if nav_instruction.value == 180 and nav_instruction.action in (
        Direction.RIGHT,
        Direction.LEFT,
    ):
        if current_direction == Direction.EAST:
            return directions[3]
        new_value = abs(current_direction_value - 2)
        return directions[new_value]
    if nav_instruction.value == 270 and nav_instruction.action == Direction.RIGHT:
        if current_direction == Direction.NORTH:
            return directions[3]
        if current_direction == Direction.EAST:
            return directions[0]
        if current_direction == Direction.SOUTH:
            return directions[1]
        if current_direction == Direction.WEST:
            return directions[2]
    if nav_instruction.value == 270 and nav_instruction.action == Direction.LEFT:
        if current_direction == Direction.NORTH:
            return directions[1]
        if current_direction == Direction.EAST:
            return directions[2]
        if current_direction == Direction.SOUTH:
            return directions[3]
        if current_direction == Direction.WEST:
            return directions[0]
    """


def handle_navigation_instruction(
    current_position: CurrentPosition,
    waypoint: WayPoint,
    nav_instruction: NavInstruction,
):
    if nav_instruction.action == Direction.NORTH:
        if waypoint.NS == Direction.SOUTH:
            value = waypoint.NS_value - nav_instruction.value
            if value < 0:
                waypoint.NS = Direction.NORTH
            waypoint.NS_value = abs(value)
        else:
            waypoint.NS_value += nav_instruction.value
    elif nav_instruction.action == Direction.SOUTH:
        if waypoint.NS == Direction.NORTH:
            value = waypoint.NS_value - nav_instruction.value
            if value < 0:
                waypoint.NS = Direction.SOUTH
            waypoint.NS_value = abs(value)
        else:
            waypoint.NS_value += nav_instruction.value
    elif nav_instruction.action == Direction.EAST:
        if waypoint.EW == Direction.WEST:
            value = waypoint.EW_value - nav_instruction.value
            if value < 0:
                waypoint.EW = Direction.EAST
            waypoint.EW_value = abs(value)
        else:
            waypoint.EW_value += nav_instruction.value
    elif nav_instruction.action == Direction.WEST:
        if waypoint.EW == Direction.EAST:
            value = waypoint.EW_value - nav_instruction.value
            if value < 0:
                waypoint.EW = Direction.WEST
            waypoint.EW_value = abs(value)
        else:
            waypoint.EW_value += nav_instruction.value
    elif nav_instruction.action == Direction.FORWARD:
        ns_value = waypoint.NS_value * nav_instruction.value
        ew_value = waypoint.EW_value * nav_instruction.value
        if waypoint.NS != current_position.NS:
            value = current_position.NS_value - ns_value
            if value < 0:
                if current_position.NS == Direction.NORTH:
                    current_position.NS = Direction.SOUTH
                elif current_position.NS == Direction.SOUTH:
                    current_position.NS = Direction.NORTH
            current_position.NS_value = abs(value)
        else:
            current_position.NS_value += ns_value
        if waypoint.EW != current_position.EW:
            value = current_position.EW_value - ew_value
            if value < 0:
                if current_position.EW == Direction.WEST:
                    current_position.EW = Direction.EAST
                elif current_position.EW == Direction.EAST:
                    current_position.EW = Direction.WEST
            current_position.EW_value = abs(value)
        else:
            current_position.EW_value += ew_value
    elif nav_instruction.action in (Direction.RIGHT, Direction.LEFT):
        waypoint.previous_direction = waypoint.direction
        get_new_direction(waypoint, nav_instruction)
    print(waypoint)
    print(current_position)


def start_navigation(navigation_instructions: List[NavInstruction]):
    current_position = CurrentPosition()
    waypoint = WayPoint()
    for nav_instruction in navigation_instructions:
        handle_navigation_instruction(current_position, waypoint, nav_instruction)
    print(
        f"Manhattan distance: {current_position.NS_value + current_position.EW_value}"
    )


def read_navigation_instructions() -> List[NavInstruction]:
    nav_instructions = list()
    nav_instruction_regex = re.compile(r"(\w)(\d{1,3})")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                if match := nav_instruction_regex.match(line.rstrip()):
                    action, value = match.groups()
                    nav_instructions.append(
                        NavInstruction(action=Direction(action), value=int(value))
                    )
    return nav_instructions


def main():
    #print(rotate((-4, -8), degrees=-90))
    nav_instructions = read_navigation_instructions()
    start_navigation(nav_instructions)


if __name__ == "__main__":
    sys.exit(main())
