#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import sys
from itertools import combinations, permutations

INPUT_FILE = "input.txt"
inputs = []

pp = pprint.PrettyPrinter(indent=4)


class OpInstruction:
    def __init__(self, op_code=None, pos_1=None, pos_2=None, pos_3=None):
        self.op_code = op_code
        self.input_position_1 = pos_1
        self.input_position_2 = pos_2
        self.output_position = pos_3

    def __str__(self):
        return (
            f"op_code: {self.op_code}, position_1: {self.input_position_1}, "
            f"position_2: {self.input_position_2}, position_3: {self.output_position}"
        )


class IntCode:
    opcodes_orig = []
    opcodes = []
    instructions = []
    ADD, MULTIPLE, HALT = (1, 2, 99)

    @classmethod
    def add(cls, input_pos_1, input_pos_2, output_pos):
        if IntCode._check_all_inputs_are_valid(input_pos_1, input_pos_2, output_pos):
            IntCode.opcodes[output_pos] = (
                IntCode.opcodes[input_pos_1] + IntCode.opcodes[input_pos_2]
            )

    @classmethod
    def multiple(cls, input_pos_1, input_pos_2, output_pos):
        if IntCode._check_all_inputs_are_valid(input_pos_1, input_pos_2, output_pos):
            IntCode.opcodes[output_pos] = (
                IntCode.opcodes[input_pos_1] * IntCode.opcodes[input_pos_2]
            )

    @staticmethod
    def _check_all_inputs_are_valid(*args):
        valid = True
        for arg in args:
            if arg is None:
                valid = False
        return valid

    @staticmethod
    def reset_memory():
        IntCode.opcodes = IntCode.opcodes_orig[:]


def read_opcodes():
    with open(INPUT_FILE, "r") as f_handle:
        opcodes = [int(number) for number in f_handle.readline().rstrip().split(",")]
    IntCode.opcodes = opcodes
    IntCode.opcodes_orig = opcodes


def parse_opcodes():
    opcodes = IntCode.opcodes
    for i in range(0, len(opcodes), 4):
        IntCode.instructions.append(OpInstruction(*opcodes[i : (i + 4)]))


def find_correct_pair_of_inputs():
    search_value = 19690720
    for pair in permutations(range(0, 100), 2):
        IntCode.opcodes[1] = pair[0]
        IntCode.opcodes[2] = pair[1]
        create_computer()
        if IntCode.opcodes[0] == search_value:
            return pair
        IntCode.reset_memory()
    print("Could not found correct value")
    return ()


def create_computer():
    for instruction in IntCode.instructions:
        if instruction.op_code == IntCode.HALT:
            return
        if instruction.op_code == IntCode.ADD:
            IntCode.add(
                instruction.input_position_1,
                instruction.input_position_2,
                instruction.output_position,
            )
        if instruction.op_code == IntCode.MULTIPLE:
            IntCode.multiple(
                instruction.input_position_1,
                instruction.input_position_2,
                instruction.output_position,
            )


def main():
    read_opcodes()
    parse_opcodes()
    value_pair = find_correct_pair_of_inputs()
    if value_pair:
        print(f"Answer is: {100* value_pair[0] + value_pair[1]}")


if __name__ == "__main__":
    sys.exit(main())
