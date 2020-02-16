#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import sys
from typing import NamedTuple

INPUT_FILE = "input.txt"
inputs = []

pp = pprint.PrettyPrinter(indent=4)

INPUT_VALUE = 5


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
    JUMP_IF_TRUE: int = 5
    JUMP_IF_FALSE: int = 6
    LESS_THAN: int = 7
    EQUALS: int = 8
    HALT: int = 99


class IntCode:
    opcodes_orig = []
    opcodes = []

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

    @classmethod
    def jump_if_true(cls, parameter_1, parameter_2):
        if IntCode.opcodes[parameter_1] != 0:
            try:
                Computer.instruction_pointer = IntCode.opcodes[parameter_2]
                return True
            except IndexError as ex:
                print(f"Could not read value from address: {parameter_2}")
                print(repr(ex))
        return False

    @classmethod
    def jump_if_false(cls, parameter_1, parameter_2):
        if IntCode.opcodes[parameter_1] == 0:
            try:
                Computer.instruction_pointer = IntCode.opcodes[parameter_2]
                return True
            except IndexError as ex:
                print(f"Could not read value from address: {parameter_2}")
                print(repr(ex))
        return False

    @classmethod
    def less_than(cls, parameter_1, parameter_2, parameter_3):
        if IntCode.opcodes[parameter_1] < IntCode.opcodes[parameter_2]:
            try:
                IntCode.opcodes[parameter_3] = 1
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))
        else:
            try:
                IntCode.opcodes[parameter_3] = 0
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))

    @classmethod
    def equals(cls, parameter_1, parameter_2, parameter_3):
        if IntCode.opcodes[parameter_1] == IntCode.opcodes[parameter_2]:
            try:
                IntCode.opcodes[parameter_3] = 1
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))
        else:
            try:
                IntCode.opcodes[parameter_3] = 0
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
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
        if str(mode)[:-2]:
            modes = f"{int(str(mode)[:-2]):03}"
        else:
            modes = "000"
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


class OpCodeInstructionProcessor:
    def process_opcode_instruction(self, opcode):
        pass


class Computer:
    instructions = []
    instruction_pointer = 0
    program_halt_flag = False
    opcode_types = OpCodeTypes()

    def has_program_halted(self):
        return self.program_halt_flag

    def interpret(self):
        while not self.has_program_halted():
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
            if attributes.opcode == self.opcode_types.HALT:
                self.program_halt_flag = True
                return
            if attributes.opcode == self.opcode_types.ADD:
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
            if attributes.opcode == self.opcode_types.MULTIPLE:
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
            if attributes.opcode == self.opcode_types.INPUT_INST:
                IntCode.input_inst(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    )
                )
                self.jump(2)
                return
            if attributes.opcode == self.opcode_types.OUTPUT_INST:
                IntCode.output(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    )
                )
                self.jump(2)
                return
            if attributes.opcode == self.opcode_types.JUMP_IF_TRUE:
                if IntCode.jump_if_true(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, Computer.instruction_pointer + 2
                    ),
                ):
                    return
                self.jump(3)
                return
            if attributes.opcode == self.opcode_types.JUMP_IF_FALSE:
                if IntCode.jump_if_false(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, Computer.instruction_pointer + 2
                    ),
                ):
                    return
                self.jump(3)
                return
            if attributes.opcode == self.opcode_types.LESS_THAN:
                IntCode.less_than(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, Computer.instruction_pointer + 2
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, Computer.instruction_pointer + 3
                    ),
                )
                self.jump(4)
                return
            if attributes.opcode == self.opcode_types.EQUALS:
                IntCode.equals(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, Computer.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, Computer.instruction_pointer + 2
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, Computer.instruction_pointer + 3
                    ),
                )
                self.jump(4)
                return

            raise AssertionError(f"Invalid opcode encountered - {attributes.opcode}")
        if opcode == self.opcode_types.HALT:
            self.program_halt_flag = True
            return
        if opcode == self.opcode_types.ADD:
            IntCode.add(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.MULTIPLE:
            IntCode.multiple(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.INPUT_INST:
            IntCode.input_inst(IntCode.opcodes[Computer.instruction_pointer + 1])
            self.jump(2)
            return
        if opcode == self.opcode_types.OUTPUT_INST:
            IntCode.output(IntCode.opcodes[Computer.instruction_pointer + 1])
            self.jump(2)
            return
        if opcode == self.opcode_types.JUMP_IF_TRUE:
            if IntCode.jump_if_true(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
            ):
                return
            self.jump(3)
            return
        if opcode == self.opcode_types.JUMP_IF_FALSE:
            if IntCode.jump_if_false(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
            ):
                return
            self.jump(3)
            return
        if opcode == self.opcode_types.LESS_THAN:
            IntCode.less_than(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.EQUALS:
            IntCode.equals(
                IntCode.opcodes[Computer.instruction_pointer + 1],
                IntCode.opcodes[Computer.instruction_pointer + 2],
                IntCode.opcodes[Computer.instruction_pointer + 3],
            )
            self.jump(4)
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
        if len(str(opcode)) >= 2:
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
