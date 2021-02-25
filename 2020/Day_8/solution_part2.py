#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import sys
from typing import List, Optional

INPUT_FILE = "input.txt"

ACCUMULATOR, JUMP, NO_OPERATION = ("acc", "jmp", "nop")


@dataclass(unsafe_hash=True)
class CPUInstruction:
    operation: str
    argument: int


@dataclass(frozen=True, eq=True)
class MemoryCache:
    instruction: CPUInstruction
    program_counter: int


class Memory:
    def __init__(self, program: List[CPUInstruction]) -> None:
        self.program = program
        self.instruction_cache: List[MemoryCache] = list()

    def get(self, index: int) -> CPUInstruction:
        try:
            return self.program[index]
        except IndexError as e:
            print(f"Cannot read instruction from place {index}")
            raise IndexError from e

    def update_instruction_cache(self, cache_value: MemoryCache):
        self.instruction_cache.append(cache_value)


class Computer:
    def __init__(self, program: List[CPUInstruction]) -> None:
        self.memory = Memory(program)
        self.program_counter = 0
        self.accumulator = 0
        self.current_instruction: Optional[CPUInstruction] = None
        self.is_running = False

    def interpret(self) -> None:
        self.is_running = True
        while self.is_running:
            instruction = self.read()
            self.update_current_instruction(instruction)
            self.update_cache_instruction()
            self.process_instruction(instruction)

    def read(self) -> CPUInstruction:
        try:
            return self.memory.get(self.program_counter)
        except IndexError:
            print("TERMINATED")
            print(f"Accumulator = {self.accumulator}")
            raise IndexError

    def update_current_instruction(self, instruction: CPUInstruction) -> None:
        self.current_instruction = instruction

    def update_cache_instruction(self) -> None:
        if self.current_instruction:
            new_cache_value = MemoryCache(
                self.current_instruction, self.program_counter
            )
            if new_cache_value in set(self.memory.instruction_cache):
                print("Same instruction being executed. Exiting...")
                self.stop_execution()
            self.memory.update_instruction_cache(new_cache_value)

    def process_instruction(self, instruction: CPUInstruction) -> None:
        if instruction.operation == NO_OPERATION:
            self.program_counter += 1
        elif instruction.operation == JUMP:
            self.jump(instruction)
        elif instruction.operation == ACCUMULATOR:
            self.update_accumulator(instruction)
        else:
            raise AssertionError(f"An invalid instruction encountered: {instruction}")

    def jump(self, instruction: CPUInstruction):
        self.program_counter += instruction.argument

    def update_accumulator(self, instruction: CPUInstruction):
        self.accumulator += instruction.argument
        self.program_counter += 1

    def stop_execution(self):
        self.is_running = False


def read_program_instructions() -> List[CPUInstruction]:
    cpu_instructions = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                operation, argument = line.rstrip().split()
                cpu_instructions.append(
                    CPUInstruction(operation=operation, argument=int(argument))
                )
    return cpu_instructions


def find_correct_operation_terminate_program(
    cpu_instructions: List[CPUInstruction],
) -> None:
    for cpu_instruction in cpu_instructions:
        if cpu_instruction.operation == JUMP:
            cpu_instruction.operation = NO_OPERATION
            computer = Computer(program=cpu_instructions)
            computer.interpret()
            cpu_instruction.operation = JUMP
        if cpu_instruction.operation == NO_OPERATION:
            cpu_instruction.operation = JUMP
            computer = Computer(program=cpu_instructions)
            computer.interpret()
            cpu_instruction.operation = NO_OPERATION


def main():
    cpu_instructions = read_program_instructions()
    find_correct_operation_terminate_program(cpu_instructions)


if __name__ == "__main__":
    sys.exit(main())
