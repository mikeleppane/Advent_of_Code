#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from functools import lru_cache
from itertools import permutations, repeat
from typing import Dict, Iterator, Union, List

INPUT_FILE = "input.txt"
NUMBER_OF_BITS = 36


class Program:
    def __init__(self):
        self.memory = {}

    def write_to_memory(self, address, value, mask):
        address_to_bits = list(f"{int(address):0>{NUMBER_OF_BITS}b}")
        mask = list(mask)
        floating_indices = []
        for index, (mask_bit, value_bit) in enumerate(zip(mask, address_to_bits)):
            if mask_bit == "X":
                floating_indices.append(index)
            elif mask_bit == "1":
                address_to_bits[index] = "1"

        for values in self.get_all_possible_values(len(floating_indices)):
            for floating_index, floating_value in zip(floating_indices, values):
                address_to_bits[floating_index] = str(floating_value)
            self.memory[int("".join(address_to_bits), 2)] = int(value)

    @lru_cache(maxsize=100)
    def get_all_possible_values(self, number_of_values):
        values = set()
        value_combinations = [
            *tuple(repeat(0, number_of_values)),
            *tuple(repeat(1, number_of_values)),
        ]
        for combination in permutations(value_combinations, number_of_values):
            values.add(combination)
        return values


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
                    match = mask_regex.match(line)
                    if match:
                        instruction["mask"] = match.groups()[0]
                    else:
                        raise ValueError("Could not parse mask line.")
                elif line.startswith("mem"):
                    match = mem_regex.match(line)
                    if match:
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
