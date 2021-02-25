#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from itertools import permutations, product
import re
import sys
from boltons.dictutils import OrderedMultiDict
from inspect import getmembers, isfunction
from pprint import PrettyPrinter
from typing import NamedTuple, Tuple, List, Iterator

INPUT_FILE = "input.txt"
ELF, GOBLIN, WALL, OPEN_CAVERN = ("elf", "goblin", "#", ".")


pp = PrettyPrinter(indent=4)


class AreaType(Enum):
    WALL = "#"
    OPEN_CAVERN = "."


class Coordinate(NamedTuple):
    x: int
    y: int


class Area(NamedTuple):
    type: str = ""


@dataclass
class Elf:
    name: str = ELF
    is_attacking: bool = False
    attack_power: int = 3
    hit_points: int = 200


@dataclass
class Goblin:
    name: str = GOBLIN
    is_attacking: bool = False
    attack_power: int = 3
    hit_points: int = 200


OPCODE, A, B, C = (0, 1, 2, 3)


class Opcode:
    def __init__(self):
        pass

    def addr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = a + b
        return output

    def addi(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = a + b
        return output

    def mulr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = a * b
        return output

    def muli(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = a * b
        return output

    def banr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = a & b
        return output

    def bani(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = a & b
        return output

    def bonr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = a | b
        return output

    def boni(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = a | b
        return output

    def setr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        output = list(register)
        output[instruction[C]] = a
        return output

    def seti(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = instruction[A]
        output = list(register)
        output[instruction[C]] = a
        return output

    def gtir(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = instruction[A]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = 1 if a > b else 0
        return output

    def gtri(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = 1 if a > b else 0
        return output

    def gtrr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = 1 if a > b else 0
        return output

    def eqir(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = instruction[A]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = 1 if a == b else 0
        return output

    def eqri(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = instruction[B]
        output = list(register)
        output[instruction[C]] = 1 if a == b else 0
        return output

    def eqrr(self, register: List[int], instruction: List[int]) -> List[int]:
        opcode = instruction[OPCODE]
        a = register[instruction[A]]
        b = register[instruction[B]]
        output = list(register)
        output[instruction[C]] = 1 if a == b else 0
        return output


def find_opcodes(instructions: OrderedMultiDict[int, str]):
    found_opcode = tuple()
    found_opcodes = {}
    while True:
        for instruction, methods in instructions.items():
            if len(methods) == 1:
                if (instruction, list(methods)[0]) not in found_opcodes:
                    found_opcode = (instruction, list(methods)[0])
                    found_opcodes[instruction] = list(methods)[0]
                break
        opcode_number, method = found_opcode
        del instructions[opcode_number]
        for i in instructions.keys():
            values = instructions[i]
            if found_opcode[1] in values:
                values = values.remove(method)
                if values:
                    instructions.update({i: values.remove(method)})

        if len(found_opcodes) == 16:
            return found_opcodes


def analyze_samples() -> OrderedMultiDict[int, str]:
    outcome = defaultdict(set)
    opcode = Opcode()
    methods = [
        func
        for func in getmembers(Opcode, predicate=isfunction)
        if func[0] != "__init__"
    ]
    for before, instruction, after in read_inputs():
        for opcode_method in methods:
            if getattr(opcode, opcode_method[0])(before, instruction) == after:
                outcome[instruction[0]].add(opcode_method[0])
    return outcome


def read_inputs() -> Iterator[Tuple[List[int]]]:
    register_regex = re.compile(r"\d{1,2}")
    with open(INPUT_FILE, "r") as f_handle:
        for lines in f_handle.read().split("\n\n"):
            lines = lines.split("\n")
            try:
                register_before = list(map(int, register_regex.findall(lines[0])))
                instruction = list(map(int, register_regex.findall(lines[1])))
                register_after = list(map(int, register_regex.findall(lines[2])))
                yield register_before, instruction, register_after
            except IndexError as ex:
                print(f"ERROR occured while processing input: {lines}")
                raise IndexError from ex


def read_test_program() -> Iterator[Tuple[List[int]]]:
    register_regex = re.compile(r"\d{1,2}")
    with open("test_program.txt", "r") as f_handle:
        for line in f_handle.read().split("\n"):
            line = line.rstrip()
            if line:
                try:
                    yield list(map(int, register_regex.findall(line)))
                except ValueError as ex:
                    print(f"ERROR occured while processing input: {line}")
                    raise ValueError from ex


def execute_test_program():
    instructions = analyze_samples()
    opcodes = find_opcodes(instructions)
    print(opcodes)
    initial_register = [0,0,0,0]
    opcode = Opcode()
    for instruction in read_test_program():
        initial_register = getattr(opcode, opcodes[instruction[0]])(initial_register, instruction)
    print(initial_register)


def main():
    execute_test_program()


if __name__ == "__main__":
    sys.exit(main())
