#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
import re
import sys
from typing import NamedTuple, Dict, Iterator, Union, List

INPUT_FILE = "input.txt"
NUMBER_OF_BITS = 36


class State(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class PocketDimension:
    cubes: Dict[Coordinate, State]


class Program:
    def __init__(self):
        self.memory = {}

    def write_to_memory(self, address, value, mask):
        value_to_bits = list(f"{int(value):0>{NUMBER_OF_BITS}b}")
        mask = list(mask)
        for index, (mask_bit, value_bit) in enumerate(zip(mask, value_to_bits)):
            if mask_bit != "X":
                if mask_bit == "1":
                    value_to_bits[index] = "1"
                else:
                    value_to_bits[index] = "0"
        self.memory[address] = int("".join(value_to_bits), 2)


def read_instructions() -> Iterator[Dict[str, Union[str, List[Dict[str, str]]]]]:
    instruction = {"mask": "", "mems": []}
    mask_regex = re.compile(r"mask\s=\s([\w\d]+)")
    mem_regex = re.compile(r"mem\[(\d+)\]\s=\s(\d+)")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                if line.startswith("mask"):
                    if instruction.get("mask"):
                        yield instruction
                    instruction = {"mask": "", "mems": []}
                    if match := mask_regex.match(line):
                        instruction["mask"] = match.groups()[0]
                    else:
                        raise ValueError("Could not parse mask line.")
                elif line.startswith("mem"):
                    if match := mem_regex.match(line):
                        instruction["mems"].append(
                            {match.groups()[0]: match.groups()[1]}
                        )
                    else:
                        raise ValueError("Could not parse mem line.")
        if instruction:
            yield instruction


def main():
    program = Program()
    for instruction in read_instructions():
        mask = instruction["mask"]
        for value_to_initialize in instruction.get("mems"):
            for memory_address, value in value_to_initialize.items():
                program.write_to_memory(address=memory_address, value=value, mask=mask)
    total = 0
    for value in program.memory.values():
        total += value
    print(total)


if __name__ == "__main__":
    sys.exit(main())
