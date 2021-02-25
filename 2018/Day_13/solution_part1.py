#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from enum import IntEnum

import sys
from itertools import product
from typing import NamedTuple, Dict, Tuple
from copy import deepcopy

INPUT_FILE = "input.txt"


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class IntersectionAction(IntEnum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 3


class Coordinate(NamedTuple):
    x: int
    y: int


@dataclass
class Track:
    part: str = ""


@dataclass
class Cart:
    direction: Direction
    mark: str = ""
    last_intersection_rule: IntersectionAction = IntersectionAction.LEFT
    ID: int = 1


TrackType = Dict[Coordinate, Track]
CartType = Dict[Coordinate, Cart]


def find_crash_location(tracks: TrackType, carts: CartType):
    new_destinations = {}
    while True:
        turn = 0
        r = set()
        for y, x in product(range(151), repeat=2):
            y, x = int(y), int(x)
            if Coordinate(x=x, y=y) in carts:
                cart = carts[Coordinate(x=x, y=y)]
                if cart.direction == Direction.UP:
                    new_destination = Coordinate(y=y - 1, x=x)
                    if turn == 0 and new_destination in carts:
                        print(len(carts))
                        print(carts)
                        del carts[new_destination]
                        del carts[(x, y)]
                        r.add(new_destination)
                        print(f"Found crash site at {new_destination}")
                        continue
                    elif turn > 0 and (new_destination in new_destinations or new_destination in carts):
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        #if new_destination in carts:
                        del carts[(x, y)]
                        #if new_destination in new_destinations:
                        #    del new_destinations[new_destination]
                        if new_destination in carts:
                            del carts[new_destination]
                        #del carts[(x, y)]
                        print(f"Found crash site at {new_destination}")
                        continue
                    next_track_part = tracks[new_destination]
                    if next_track_part.part == "|":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.UP,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "/":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.LEFT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "\\":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.RIGHT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "+":
                        direction = ""
                        action = 0
                        if cart.last_intersection_rule == IntersectionAction.LEFT:
                            direction = Direction.RIGHT
                            action = IntersectionAction.STRAIGHT
                        elif cart.last_intersection_rule == IntersectionAction.STRAIGHT:
                            direction = Direction.UP
                            action = IntersectionAction.RIGHT
                        elif cart.last_intersection_rule == IntersectionAction.RIGHT:
                            direction = Direction.LEFT
                            action = IntersectionAction.LEFT
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=direction,
                            last_intersection_rule=action,
                            ID=cart.ID,
                        )
                    turn += 1
                    continue
                elif cart.direction == Direction.DOWN:
                    new_destination = Coordinate(y=y + 1, x=x)
                    if turn == 0 and new_destination in carts:
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        del carts[new_destination]
                        del carts[(x, y)]
                        print(f"Found crash site at {new_destination}")
                        continue
                    elif turn > 0 and (new_destination in new_destinations or new_destination in carts):
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        #if new_destination in carts:
                        del carts[(x, y)]
                        #if new_destination in new_destinations:
                        #    del new_destinations[new_destination]
                        if new_destination in carts:
                            del carts[new_destination]
                        #del carts[(x, y)]
                        print(f"Found crash site at {new_destination}")
                        continue
                    next_track_part = tracks[new_destination]
                    if next_track_part.part == "|":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.DOWN,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "/":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.RIGHT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "\\":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.LEFT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "+":
                        direction = ""
                        action = 0
                        if cart.last_intersection_rule == IntersectionAction.LEFT:
                            direction = Direction.LEFT
                            action = IntersectionAction.STRAIGHT
                        elif cart.last_intersection_rule == IntersectionAction.STRAIGHT:
                            direction = Direction.DOWN
                            action = IntersectionAction.RIGHT
                        elif cart.last_intersection_rule == IntersectionAction.RIGHT:
                            direction = Direction.RIGHT
                            action = IntersectionAction.LEFT
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=direction,
                            last_intersection_rule=action,
                            ID=cart.ID,
                        )
                    turn += 1
                    continue
                elif cart.direction == Direction.LEFT:
                    new_destination = Coordinate(y=y, x=x + 1)
                    if turn == 0 and new_destination in carts:
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        del carts[new_destination]
                        del carts[(x, y)]
                        print(f"Found crash site at {new_destination}")
                        continue
                    elif turn > 0 and (new_destination in new_destinations or new_destination in carts):
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        #if new_destination in carts:
                        del carts[(x, y)]
                        #if new_destination in new_destinations:
                        #    del new_destinations[new_destination]
                        if new_destination in carts:
                            del carts[new_destination]
                        print(f"Found crash site at {new_destination}")
                        continue
                    next_track_part = tracks[new_destination]
                    if next_track_part.part == "-":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.LEFT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "/":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.UP,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "\\":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.DOWN,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "+":
                        direction = ""
                        action = 0
                        if cart.last_intersection_rule == IntersectionAction.LEFT:
                            direction = Direction.UP
                            action = IntersectionAction.STRAIGHT
                        elif cart.last_intersection_rule == IntersectionAction.STRAIGHT:
                            direction = Direction.LEFT
                            action = IntersectionAction.RIGHT
                        elif cart.last_intersection_rule == IntersectionAction.RIGHT:
                            direction = Direction.DOWN
                            action = IntersectionAction.LEFT
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=direction,
                            last_intersection_rule=action,
                            ID=cart.ID,
                        )
                    turn += 1
                    continue
                elif cart.direction == Direction.RIGHT:
                    new_destination = Coordinate(y=y, x=x - 1)
                    if turn == 0 and new_destination in carts:
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        del carts[new_destination]
                        del carts[(x, y)]
                        print(f"Found crash site at {new_destination}")
                        continue
                    elif turn > 0 and (new_destination in new_destinations or new_destination in carts):
                        print(len(carts))
                        print(carts)
                        r.add(new_destination)
                        #if new_destination in carts:
                        del carts[(x, y)]
                        #if new_destination in new_destinations:
                        #    del new_destinations[new_destination]
                        if new_destination in carts:
                            del carts[new_destination]
                        print(f"Found crash site at {new_destination}")
                        continue
                    next_track_part = tracks[new_destination]
                    if next_track_part.part == "-":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.RIGHT,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )
                    elif next_track_part.part == "/":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.DOWN,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )

                    elif next_track_part.part == "\\":
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=Direction.UP,
                            last_intersection_rule=cart.last_intersection_rule,
                            ID=cart.ID,
                        )

                    elif next_track_part.part == "+":
                        direction = ""
                        action = 0
                        if cart.last_intersection_rule == IntersectionAction.LEFT:
                            direction = Direction.DOWN
                            action = IntersectionAction.STRAIGHT
                        elif cart.last_intersection_rule == IntersectionAction.STRAIGHT:
                            direction = Direction.RIGHT
                            action = IntersectionAction.RIGHT
                        elif cart.last_intersection_rule == IntersectionAction.RIGHT:
                            direction = Direction.UP
                            action = IntersectionAction.LEFT
                        new_destinations[new_destination] = Cart(
                            mark=next_track_part.part,
                            direction=direction,
                            last_intersection_rule=action,
                            ID=cart.ID,
                        )
                    turn += 1
                    continue
        for u in r:
            if u in new_destinations:
                del new_destinations[u]
        if len(new_destinations) == 1:
            print(carts)
        carts = deepcopy(new_destinations)
        if len(carts) == 1:
            print(carts)
            print(new_destinations)
            return
        #carts = deepcopy(new_destinations)
        new_destinations.clear()


def read_track() -> Tuple[TrackType, CartType]:
    tracks = {}
    carts = {}
    ID = 1
    with open(INPUT_FILE, "r") as f_handle:
        for y, line in enumerate(f_handle):
            line = line.rstrip("\n")
            if line:
                for x, part in enumerate(line):
                    if part.strip():
                        if part in ("<", ">", "v", "^"):
                            if part == "<":
                                carts[Coordinate(x=x, y=y)] = Cart(
                                    mark=part, direction=Direction.RIGHT, ID=ID
                                )
                                tracks[Coordinate(x=x, y=y)] = Track(part="-")
                                ID += 1
                            elif part == ">":
                                carts[Coordinate(x=x, y=y)] = Cart(
                                    mark=part, direction=Direction.LEFT, ID=ID
                                )
                                tracks[Coordinate(x=x, y=y)] = Track(part="-")
                                ID += 1
                            elif part == "v":
                                carts[Coordinate(x=x, y=y)] = Cart(
                                    mark=part, direction=Direction.DOWN, ID=ID
                                )
                                tracks[Coordinate(x=x, y=y)] = Track(part="|")
                                ID += 1
                            elif part == "^":
                                carts[Coordinate(x=x, y=y)] = Cart(
                                    mark=part, direction=Direction.UP, ID=ID
                                )
                                tracks[Coordinate(x=x, y=y)] = Track(part="|")
                                ID += 1
                        else:
                            tracks[Coordinate(x=x, y=y)] = Track(part=part)
    return tracks, carts


def main():
    tracks, carts = read_track()
    find_crash_location(tracks, carts)


if __name__ == "__main__":
    sys.exit(main())
