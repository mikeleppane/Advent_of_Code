#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#from dataclasses import dataclass

import re
import sys
from pprint import PrettyPrinter
from typing import Tuple, List

INPUT_FILE = "input.txt"


pp = PrettyPrinter(indent=4)

A, B, C = (0, 1, 2)

#@dataclass
class InstructionPointer:
    def __init__(self, value, bound):
        self.value = value
        self.bound = bound

    def incr(self, value=None):
        if value:
            self.value += value
        else:
            self.value += 1


#@dataclass
class Instruction:
    def __init__(self, name, instruction):
        self.name = name
        self.instructions = instruction


class Opcode:
    def __init__(self, register: List[int]):
        self.register = list(register)
        self.ip = InstructionPointer(value=0, bound=0)

    def update_register(self, value):
        self.register[self.ip.bound] = value

    def addr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = a + b

    def addi(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = a + b

    def mulr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = a * b

    def muli(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = a * b

    def banr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = a & b

    def bani(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = a & b

    def bonr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = a | b

    def boni(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = a | b

    def setr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        self.register[instruction[C]] = a

    def seti(self, instruction: List[int]):
        a = instruction[A]
        self.register[instruction[C]] = a

    def gtir(self, instruction: List[int]):
        a = instruction[A]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = 1 if a > b else 0

    def gtri(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = 1 if a > b else 0

    def gtrr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = 1 if a > b else 0

    def eqir(self, instruction: List[int]):
        a = instruction[A]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = 1 if a == b else 0

    def eqri(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = instruction[B]
        self.register[instruction[C]] = 1 if a == b else 0

    def eqrr(self, instruction: List[int]):
        a = self.register[instruction[A]]
        b = self.register[instruction[B]]
        self.register[instruction[C]] = 1 if a == b else 0


def execute_program():
    opcode = Opcode(register=[0, 100000000, 2, 10551288, 1, 0])
    ip, instructions = read_instructions()
    opcode.ip.bound = ip
    opcode.ip.value = 3
    while True:
        if opcode.ip.value >= len(instructions):
            print(opcode.register)
            raise ValueError("OVERFLOW")
        opcode.update_register(opcode.ip.value)
        instruction = instructions[opcode.ip.value]
        getattr(opcode, instruction.name)(instruction.instructions)
        opcode.ip.value = opcode.register[opcode.ip.bound]
        opcode.ip.value += 1
        print(opcode.register)
        print(opcode.ip.value)
        #print()

def read_instructions() -> Tuple[int, List[Instruction]]:
    instructions = list()
    instruction_regex = re.compile(r"\d{1,2}")
    opcode_name_regex = re.compile(r"\w+")
    with open(INPUT_FILE, "r") as f_handle:
        lines = f_handle.read().split("\n")
        ip = list(map(int, instruction_regex.findall(lines[0].rstrip())))[0]
        for line in lines[1:]:
            line = line.rstrip()
            opcode_name = opcode_name_regex.match(line).group()
            instruction = list(map(int, instruction_regex.findall(line)))
            instructions.append(Instruction(name=opcode_name, instruction=instruction))
    return ip, instructions


def main():
    execute_program()


if __name__ == "__main__":
    sys.exit(main())
