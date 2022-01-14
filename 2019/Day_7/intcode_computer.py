#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
from typing import NamedTuple
from collections import deque


INPUT_FILE = "input.txt"
inputs = []

pp = pprint.PrettyPrinter(indent=4)


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
    def __init__(self, opcodes):
        self.opcodes_orig = list(opcodes)
        self.opcodes = list(opcodes)

    def add(self, input_pos_1, input_pos_2, output_pos):
        if self._check_all_inputs_are_valid(input_pos_1, input_pos_2, output_pos):
            self.opcodes[output_pos] = (
                self.opcodes[input_pos_1] + self.opcodes[input_pos_2]
            )

    def multiple(self, input_pos_1, input_pos_2, output_pos):
        if self._check_all_inputs_are_valid(input_pos_1, input_pos_2, output_pos):
            self.opcodes[output_pos] = (
                self.opcodes[input_pos_1] * self.opcodes[input_pos_2]
            )

    def input_inst(self, address, value):
        try:
            self.opcodes[address] = value
        except IndexError as ex:
            print(f"Could not store value to address: {address}")
            print(repr(ex))

    def output(self, input_value):
        #print(self.opcodes[input_value])
        try:
            return self.opcodes[input_value]
        except IndexError as ex:
            print(f"Could not read value from address: {input_value}")
            print(repr(ex))

    def jump_if_true(self, parameter_1):
        if self.opcodes[parameter_1] != 0:
            return True
        return False

    def jump_if_false(self, parameter_1):
        if self.opcodes[parameter_1] == 0:
            return True
        return False

    def less_than(self, parameter_1, parameter_2, parameter_3):
        if self.opcodes[parameter_1] < self.opcodes[parameter_2]:
            try:
                self.opcodes[parameter_3] = 1
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))
        else:
            try:
                self.opcodes[parameter_3] = 0
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))

    def equals(self, parameter_1, parameter_2, parameter_3):
        if self.opcodes[parameter_1] == self.opcodes[parameter_2]:
            try:
                self.opcodes[parameter_3] = 1
            except IndexError as ex:
                print(f"Could not store value to address: {parameter_3}")
                print(repr(ex))
        else:
            try:
                self.opcodes[parameter_3] = 0
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

    def reset_memory(self):
        self.opcodes = self.opcodes_orig[:]


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
    def __init__(self, opcodes):
        self.intcode = IntCode(opcodes)
        self.instructions = []
        self.instruction_pointer = 0
        self.program_halt_flag = False
        self.opcode_types = OpCodeTypes()
        self._input_values = deque()
        self._output = None
        self.initial_input = None
        self.halted = False

    @property
    def input_values(self):
        if self._input_values:
            return self._input_values.popleft()
        self.program_halt_flag = True

    @input_values.setter
    def input_values(self, value):
        self._input_values.append(value)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    def has_program_halted(self):
        return self.program_halt_flag

    def interpret(self):
        while not self.has_program_halted():
            if self.halted:
                return
            self.execute_instruction(self.read())

    def read(self):
        return self.intcode.opcodes[self.instruction_pointer]

    def jump(self, value):
        self.instruction_pointer += value

    def reset_halt_flag(self):
        self.program_halt_flag = False

    def reset(self):
        self.intcode.reset_memory()
        self.instruction_pointer = 0
        self.program_halt_flag = False
        self._input_values = deque()
        self.halted = False

    def execute_instruction(self, opcode):
        if self._is_parameter_mode(opcode):
            attributes = ParameterModeHandler().get_parameter_attributes(opcode)
            if attributes.opcode == self.opcode_types.HALT:
                self.program_halt_flag = True
                self.halted = True
                return
            if attributes.opcode == self.opcode_types.ADD:
                self.intcode.opcodes[
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, self.instruction_pointer + 3
                    )
                ] = (
                    self.intcode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_1, self.instruction_pointer + 1,
                        )
                    ]
                    + self.intcode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_2, self.instruction_pointer + 2,
                        )
                    ]
                )
                self.jump(4)
                return
            if attributes.opcode == self.opcode_types.MULTIPLE:
                self.intcode.opcodes[
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, self.instruction_pointer + 3
                    )
                ] = (
                    self.intcode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_1, self.instruction_pointer + 1,
                        )
                    ]
                    * self.intcode.opcodes[
                        self._get_correct_parameter_mode(
                            attributes.mode_parameter_2, self.instruction_pointer + 2,
                        )
                    ]
                )
                self.jump(4)
                return
            if attributes.opcode == self.opcode_types.INPUT_INST:
                if self._input_values:
                    input_value = self.input_values
                else:
                    self.program_halt_flag = True
                    return
                self.intcode.input_inst(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    ),
                    input_value,
                )
                self.jump(2)
                return
            if attributes.opcode == self.opcode_types.OUTPUT_INST:
                self.output = self.intcode.output(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    )
                )
                self.jump(2)
                self.program_halt_flag = True
                return
            if attributes.opcode == self.opcode_types.JUMP_IF_TRUE:
                if self.intcode.jump_if_true(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    ),
                ):
                    try:
                        self.instruction_pointer = self.intcode.opcodes[
                            self._get_correct_parameter_mode(
                                attributes.mode_parameter_2,
                                self.instruction_pointer + 2,
                            )
                        ]
                    except IndexError as ex:
                        print(f"Could not read value from address")
                        print(repr(ex))
                    return
                self.jump(3)
                return
            if attributes.opcode == self.opcode_types.JUMP_IF_FALSE:
                if self.intcode.jump_if_false(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    ),
                ):
                    try:
                        self.instruction_pointer = self.intcode.opcodes[
                            self._get_correct_parameter_mode(
                                attributes.mode_parameter_2,
                                self.instruction_pointer + 2,
                            )
                        ]
                    except IndexError as ex:
                        print(f"Could not read value from address")
                        print(repr(ex))
                    return
                self.jump(3)
                return
            if attributes.opcode == self.opcode_types.LESS_THAN:
                self.intcode.less_than(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, self.instruction_pointer + 2
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, self.instruction_pointer + 3
                    ),
                )
                self.jump(4)
                return
            if attributes.opcode == self.opcode_types.EQUALS:
                self.intcode.equals(
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_1, self.instruction_pointer + 1
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_2, self.instruction_pointer + 2
                    ),
                    self._get_correct_parameter_mode(
                        attributes.mode_parameter_3, self.instruction_pointer + 3
                    ),
                )
                self.jump(4)
                return

            raise AssertionError(f"Invalid opcode encountered - {attributes.opcode}")
        if opcode == self.opcode_types.HALT:
            self.program_halt_flag = True
            return
        if opcode == self.opcode_types.ADD:
            self.intcode.add(
                self.intcode.opcodes[self.instruction_pointer + 1],
                self.intcode.opcodes[self.instruction_pointer + 2],
                self.intcode.opcodes[self.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.MULTIPLE:
            self.intcode.multiple(
                self.intcode.opcodes[self.instruction_pointer + 1],
                self.intcode.opcodes[self.instruction_pointer + 2],
                self.intcode.opcodes[self.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.INPUT_INST:
            if self._input_values:
                input_value = self.input_values
            else:
                self.program_halt_flag = True
                return
            self.intcode.input_inst(
                self.intcode.opcodes[self.instruction_pointer + 1], input_value
            )
            self.jump(2)
            return
        if opcode == self.opcode_types.OUTPUT_INST:
            self._output = self.intcode.output(
                self.intcode.opcodes[self.instruction_pointer + 1]
            )
            self.jump(2)
            self.program_halt_flag = True
            return
        if opcode == self.opcode_types.JUMP_IF_TRUE:
            if self.intcode.jump_if_true(
                self.intcode.opcodes[self.instruction_pointer + 1],
            ):
                try:
                    self.instruction_pointer = self.intcode.opcodes[
                        self.intcode.opcodes[self.instruction_pointer + 2]
                    ]
                except IndexError as ex:
                    print(f"Could not read value from address")
                    print(repr(ex))
                return
            self.jump(3)
            return
        if opcode == self.opcode_types.JUMP_IF_FALSE:
            if self.intcode.jump_if_false(
                self.intcode.opcodes[self.instruction_pointer + 1],
            ):
                try:
                    self.instruction_pointer = self.intcode.opcodes[
                        self.intcode.opcodes[self.instruction_pointer + 2]
                    ]
                except IndexError as ex:
                    print(f"Could not read value from address")
                    print(repr(ex))
                return
            self.jump(3)
            return
        if opcode == self.opcode_types.LESS_THAN:
            self.intcode.less_than(
                self.intcode.opcodes[self.instruction_pointer + 1],
                self.intcode.opcodes[self.instruction_pointer + 2],
                self.intcode.opcodes[self.instruction_pointer + 3],
            )
            self.jump(4)
            return
        if opcode == self.opcode_types.EQUALS:
            self.intcode.equals(
                self.intcode.opcodes[self.instruction_pointer + 1],
                self.intcode.opcodes[self.instruction_pointer + 2],
                self.intcode.opcodes[self.instruction_pointer + 3],
            )
            self.jump(4)
            return
        raise AssertionError(f"Invalid opcode encountered - {opcode}")

    def _get_correct_parameter_mode(self, mode, address):
        parameter_handler = ParameterModeHandler()
        if parameter_handler.is_position_mode(mode):
            return self.intcode.opcodes[address]
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
    return opcodes
