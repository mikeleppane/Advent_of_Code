#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum

from itertools import cycle
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


@dataclass(frozen=True, eq=True)
class NavInstruction:
    action: Direction
    value: int


def get_new_direction(
    current_direction: Direction, nav_instruction: NavInstruction
) -> Direction:
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

def handle_navigation_instruction(
    current_position: CurrentPosition, nav_instruction: NavInstruction
):
    if nav_instruction.action == Direction.NORTH:
        if current_position.NS == Direction.SOUTH:
            value = current_position.NS_value - nav_instruction.value
            if value < 0:
                current_position.NS = Direction.NORTH
            current_position.NS_value = abs(value)
        else:
            current_position.NS_value += nav_instruction.value
    elif nav_instruction.action == Direction.SOUTH:
        if current_position.NS == Direction.NORTH:
            value = current_position.NS_value - nav_instruction.value
            if value < 0:
                current_position.NS = Direction.SOUTH
            current_position.NS_value = abs(value)
        else:
            current_position.NS_value += nav_instruction.value
    elif nav_instruction.action == Direction.EAST:
        if current_position.EW == Direction.WEST:
            value = current_position.EW_value - nav_instruction.value
            if value < 0:
                current_position.EW = Direction.EAST
            current_position.EW_value = abs(value)
        else:
            current_position.EW_value += nav_instruction.value
    elif nav_instruction.action == Direction.WEST:
        if current_position.EW == Direction.EAST:
            value = current_position.EW_value - nav_instruction.value
            if value < 0:
                current_position.EW = Direction.WEST
            current_position.EW_value = abs(value)
        else:
            current_position.EW_value += nav_instruction.value
    elif nav_instruction.action == Direction.FORWARD:
        if current_position.direction in (Direction.NORTH, Direction.SOUTH):
            if current_position.direction != current_position.NS:
                value = current_position.NS_value - nav_instruction.value
                if value < 0:
                    if current_position.NS == Direction.NORTH:
                        current_position.NS = Direction.SOUTH
                    elif current_position.NS == Direction.SOUTH:
                        current_position.NS = Direction.NORTH
                current_position.NS_value = abs(value)
            else:
                current_position.NS_value += nav_instruction.value
        if current_position.direction in (Direction.EAST, Direction.WEST):
            if current_position.direction != current_position.EW:
                value = current_position.EW_value - nav_instruction.value
                if value <= 0:
                    if current_position.EW == Direction.WEST:
                        current_position.EW = Direction.EAST
                    elif current_position.EW == Direction.EAST:
                        current_position.EW = Direction.WEST
                current_position.EW_value = abs(value)
            else:
                current_position.EW_value += nav_instruction.value
    elif nav_instruction.action in (Direction.RIGHT, Direction.LEFT):
        current_position.previous_direction = current_position.direction
        current_position.direction = get_new_direction(
            current_position.direction, nav_instruction
        )
    print(current_position)


def start_navigation(navigation_instructions: List[NavInstruction]):
    current_position = CurrentPosition()
    for nav_instruction in navigation_instructions:
        handle_navigation_instruction(current_position, nav_instruction)
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
    nav_instructions = read_navigation_instructions()
    start_navigation(nav_instructions)


if __name__ == "__main__":
    sys.exit(main())
