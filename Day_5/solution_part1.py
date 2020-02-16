#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import sys
from typing import NamedTuple

INPUT_FILE = "input.txt"
inputs = []

pp = pprint.PrettyPrinter(indent=4)

ADD, MULTIPLE, INPUT_INST, OUTPUT_INST, HALT = (1, 2, 3, 4, 99)

INPUT_VALUE = 1


class ParameterModeAttributes(NamedTuple):
    opcode: int
    mode_parameter_1: int
    mode_parameter_2: int
    mode_parameter_3: int

class OpCodeTypes(NamedTuple):
    ADD: int = 1
    MULTIPLE: int = 2
    INPUT_INST: int = 3
    OUTPUT_INST: int = 4
    HALT: int = 99



class IntCode:
    opcodes_orig = []
    opcodes = []
    instructions = []

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

    @classmethod
    def input_inst(cls, address):
        try:
            IntCode.opcodes[address] = INPUT_VALUE
        except IndexError as ex:
            print(f"Could not store value to address: {address}")
            print(repr(ex))

    @classmethod
    def output(cls, input_value):
        print(IntCode.opcodes[input_value])
        try:
            return IntCode.opcodes[input_value]
        except IndexError as ex:
            print(f"Could not read value from address: {input_value}")
            print(repr(ex))

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


class ParameterModeHandler:
    POSITION_MODE, IMMEDIATE_MODE = (0, 1)

    def get_parameter_attributes(self, mode):
        return self._parse_mode(mode)

    @staticmethod
    def _parse_mode(mode):
        opcode = int(str(mode)[-2:])
        modes = f"{int(str(mode)[:-2]):03}"
        return ParameterModeAttributes(
            opcode,
            mode_parameter_1=int(modes[-1]),
            mode_parameter_2=int(modes[1]),
            mode_parameter_3=int(modes[0]),
        )

    def is_position_mode(self, mode):
        return self.POSITION_MODE == mode

    def is_immediate_mode(self, mode):
        return self.IMMEDIATE_MODE == mode


class Computer:
    instructions = []
    instruction_pointer = 0
    stop_flag = False
    ADD, MULTIPLE, INPUT_INST, OUTPUT_INST, HALT = (1, 2, 3, 4, 99)

    def interpret(self):
        while self.stop_flag is False:
            self.execute_instruction(self.read())

    @staticmethod
    def read():
        return IntCode.opcodes[Computer.instruction_pointer]

    @staticmethod
    def jump(value):
        Computer.instruction_pointer += value

    def execute_instruction(self, opcode):
        if self._is_parameter_mode(opcode):
            attributes = ParameterModeHandler().get_parameter_attributes(opcode)
            if attributes.opcode == self.HALT:
                self.stop_flag = True
                return
            if attributes.opcode == self.ADD:
                IntCode.opcodes[
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, Computer.instruction_pointer + 3
                    )
                ] = (
                    IntCode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_1,
                            Computer.instruction_pointer + 1,
                        )
                    ]
                    + IntCode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_2,
                            Computer.instruction_pointer + 2,
                        )
                    ]
                )
                self.jump(4)
                return
            if attributes.opcode == self.MULTIPLE:
                IntCode.opcodes[
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, Computer.instruction_pointer + 3
                    )
                ] = (
                    IntCode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_1,
                            Computer.instruction_pointer + 1,
                        )
                    ]
                    * IntCode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_2,
                            Computer.instruction_pointer + 2,
                        )
                    ]
                )
                self.jump(4)
                return
            if attributes.opcode == self.INPUT_INST:
                IntCode.input_inst(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    )
                )
                self.jump(2)
                return
            if attributes.opcode == self.OUTPUT_INST:
                IntCode.output(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    )
                )
                self.jump(2)
                return
            raise AssertionError(f"Invalid opcode encountered - {attributes.opcode}")
        if opcode == self.HALT:
            self.stop_flag = True
            return
        if opcode == self.ADD:
            IntCode.add(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.MULTIPLE:
            IntCode.multiple(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.INPUT_INST:
            IntCode.input_inst(IntCode.opcodes[Computer.instruction_pointer + 1])
            self.jump(2)
            return
        if opcode == self.OUTPUT_INST:
            IntCode.output(IntCode.opcodes[Computer.instruction_pointer + 1])
            self.jump(2)
            return
        raise AssertionError(f"Invalid opcode encountered - {opcode}")

    def _get_correct_parameter_mode(self, mode, address):
        parameter_handler = ParameterModeHandler()
        if parameter_handler.is_position_mode(mode):
            return IntCode.opcodes[address]
        else:
            return address

    @staticmethod
    def _is_parameter_mode(opcode):
        if len(str(opcode)) >= 3:
            return True
        return False


def read_opcodes():
    with open(INPUT_FILE, "r") as f_handle:
        opcodes = [int(number) for number in f_handle.readline().rstrip().split(",")]
    IntCode.opcodes = opcodes
    IntCode.opcodes_orig = list(opcodes)


def main():
    read_opcodes()
    computer = Computer()
    computer.interpret()


if __name__ == "__main__":
    sys.exit(main())
