#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import count
from typing import List, Union, NamedTuple

INPUT_FILE = "input.txt"


class BusID(NamedTuple):
    ID: Union[str, int]
    offset: int


def find_earliest_timestamp(bus_ids: List[BusID]) -> int:
    timestamp = 0
    for value in count(start=305000000000007, step=bus_ids[0].ID):
        timestamp = value
        if all(
            {(timestamp + bus_id.offset) % bus_id.ID == 0 for bus_id in bus_ids[1:]}
        ):
            if (timestamp + bus_ids[-1].offset) % bus_ids[0].ID == 0:
                timestamp += bus_ids[-1].offset
            break
    return timestamp


def read_bus_schedules() -> List[BusID]:
    bus_ids = list()
    with open(INPUT_FILE, "r") as f_handle:
        for i, line in enumerate(f_handle):
            if i > 0:
                for index, _id in enumerate(line.rstrip().split(",")):
                    if _id == "x":
                        continue
                    if _id.isdigit():
                        bus_ids.append(BusID(offset=index, ID=int(_id)))

    return bus_ids


def main():
    ids = read_bus_schedules()
    print(f"Earliest timestamp: {find_earliest_timestamp(bus_ids=ids)}")


if __name__ == "__main__":
    sys.exit(main())
