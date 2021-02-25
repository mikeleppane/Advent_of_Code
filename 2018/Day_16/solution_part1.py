#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from enum import Enum
from inspect import getmembers, isfunction
import sys
import re
from pprint import PrettyPrinter
from typing import NamedTuple, Tuple, List
from boltons.dictutils import OrderedMultiDict

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


def analyze_samples():
    outcome = OrderedMultiDict()
    opcode = Opcode()
    methods = [
        func
        for func in getmembers(Opcode, predicate=isfunction)
        if func[0] != "__init__"
    ]
    count = 0
    for before, instruction, after in read_inputs():
        outcome.clear()
        for opcode_method in methods:
            if getattr(opcode, opcode_method[0])(before, instruction) == after:
                outcome.add(instruction[0], opcode_method[0])
        if len(outcome.getlist(instruction[0])) >= 3:
            count += 1
    #print(outcome)
    print(count)


def read_inputs():
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

    return


def main():
    analyze_samples()


if __name__ == "__main__":
    sys.exit(main())
