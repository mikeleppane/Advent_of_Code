#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import sys
from itertools import count
from typing import List, Tuple, Union

INPUT_FILE = "input.txt"


@dataclass(frozen=True, eq=True)
class BusSchedule:
    timestamp: int
    ids: List[int]


def get_closest_time(_id: int, timestamp: int) -> int:
    for value in count(start=0, step=_id):
        if value >= timestamp:
            return value
    return -1


def find_earliest_bus(schedule: BusSchedule) -> Tuple[Union[int, float], int]:
    min_closest_time = float("inf")
    id_for_min_closest_time = -1
    for bus_id in schedule.ids:
        closest_time_for_id = get_closest_time(bus_id, schedule.timestamp)
        if closest_time_for_id >= schedule.timestamp:
            if closest_time_for_id < min_closest_time:
                id_for_min_closest_time = bus_id
                min_closest_time = closest_time_for_id
    return min_closest_time, id_for_min_closest_time


def read_bus_schedules() -> BusSchedule:
    timestamp = 0
    ids = list()
    with open(INPUT_FILE, "r") as f_handle:
        for index, line in enumerate(f_handle):
            if index == 0:
                if line:
                    timestamp = int(line.rstrip())
            else:
                ids = [int(_id) for _id in line.rstrip().split(",") if _id != "x"]

    return BusSchedule(timestamp=timestamp, ids=ids)


def main():
    schelude = read_bus_schedules()
    min_time, _id = find_earliest_bus(schelude)
    print(f"Result: {(min_time - schelude.timestamp) * _id}")


if __name__ == "__main__":
    sys.exit(main())
