#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import re
import sys
from boltons.dictutils import OrderedMultiDict
from boltons.setutils import IndexedSet
from collections import deque

INPUT_FILE = "input.txt"


@dataclass
class Worker:
    instruction: str = ""
    start_time: int = 0


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


def get_step_time(letter, offset=0):
    return (ord(letter) - 64) + offset


class WorkerManager:
    max_len = 5

    def __init__(self, offset):
        self.offset = offset
        self.workers = {}
        self.start_time = 0

    def add(self, instruction):
        if len(self.workers) < WorkerManager.max_len and instruction not in self.workers:
            self.workers[instruction] = self.start_time

    def remove(self, instruction):
        if instruction in self.workers:
            worker_start_time = self.workers[instruction]
            delta = self.get_step_time(instruction) + worker_start_time
            if delta > self.start_time:
                self.start_time += self.get_step_time(instruction) - self.start_time
            #else:
            #    self.start_time += self.get_step_time(instruction)
            del self.workers[instruction]
        print(self.start_time)

    @staticmethod
    def get_step_time(letter, offset=60):
        return (ord(letter) - 64) + offset


def find_instruction_order(instructions: OrderedMultiDict):
    starting_instruction = set(instructions.keys(multi=True)).difference(
        set(instructions.values(multi=True))
    )
    worker_manager = WorkerManager(offset=0)
    instruction_order = IndexedSet()
    current_instructions = list()
    for index, value in enumerate(sorted(starting_instruction)):
        current_instructions.append(value)
        worker_manager.add(value)
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
                worker_manager.remove(current_instruction)
                for n, value in enumerate(instructions.getlist(current_instruction)):
                    if value not in current_instructions:
                        current_instructions.append(value)
                index = i
                break
        if index != -1:
            current_instructions.pop(index)
        current_instructions = sorted(current_instructions)
        for instruction in current_instructions:
            worker_manager.add(instruction)
    print("".join(instruction_order))
    print(worker_manager.start_time)


def main():
    instructions = read_instructions()
    find_instruction_order(instructions)


if __name__ == "__main__":
    sys.exit(main())
