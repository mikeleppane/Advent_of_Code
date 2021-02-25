#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import sys
from boltons.dictutils import OrderedMultiDict
from boltons.setutils import IndexedSet

INPUT_FILE = "input.txt"


def read_instructions() -> OrderedMultiDict[str, str]:
    instructions = OrderedMultiDict()
    instruction_regex = re.compile(r"\s(\w)\s")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                key, value = instruction_regex.findall(line.rstrip())
                if key not in instructions:
                    instructions[key] = value
                else:
                    instructions.add(key, value)
    return instructions


def find_instruction_order(instructions: OrderedMultiDict):
    starting_instruction = set(instructions.keys(multi=True)).difference(
        set(instructions.values(multi=True))
    )
    instruction_order = IndexedSet()
    current_instructions = list()
    for value in sorted(starting_instruction):
        current_instructions.append(value)
    current_instructions = sorted(current_instructions)
    while current_instructions:
        index = -1
        for i, current_instruction in enumerate(current_instructions):
            if not {
                key
                for key, value in instructions.items(multi=True)
                if value == current_instruction
            }.difference(instruction_order):
                instruction_order.add(current_instruction)
                for value in instructions.getlist(current_instruction):
                    if value not in current_instructions:
                        current_instructions.append(value)
                index = i
                break
        if index != -1:
            current_instructions.pop(index)
        current_instructions = sorted(current_instructions)
    print("".join(instruction_order))


def main():
    instructions = read_instructions()
    find_instruction_order(instructions)


if __name__ == "__main__":
    sys.exit(main())
