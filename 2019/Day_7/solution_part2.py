#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import permutations

from intcode_computer import Computer, read_opcodes

INPUT_FILE = "input.txt"


class Amplifier:
    def __init__(self, name, amplifier_software, phase_setting=None, input_signal=None):
        self.amplifier_name = name
        self._phase_setting = phase_setting
        self._input_signal = input_signal
        self._output_signal = 0
        self.intcode_computer: Computer = Computer(amplifier_software)

    @property
    def output_signal(self):
        return self._output_signal

    @property
    def input_signal(self):
        return self._input_signal

    @input_signal.setter
    def input_signal(self, value):
        self._input_signal = value

    @property
    def phase_setting(self):
        return self._phase_setting

    @phase_setting.setter
    def phase_setting(self, value):
        self._phase_setting = value

    def __str__(self):
        return (
            f"{self.__class__.__name__}(amplifier_name={self.amplifier_name},"
            f"phase_setting={self.phase_setting},"
            f"input_signal={self.input_signal})"
        )

    def __repr__(self):
        return self.__str__()


class ThrusterOptimizer:
    phase_setting_options = [5, 6, 7, 8, 9]

    def __init__(self):
        self.max_output = 0
        self.amplifiers = list()

    def initialize(self):
        opcodes = read_opcodes()
        for name in ("A", "B", "C", "D", "E"):
            self.amplifiers.append(Amplifier(name=name, amplifier_software=opcodes))

    def optimize_thrust(self):
        for phase_setting in self.get_all_combinations():
            print(phase_setting)
            self.process_amplifier_pipeline(phase_setting)

    def process_amplifier_pipeline(self, phase_setting):
        output = 0
        has_a_amplifier_initialized = False
        is_phase_initialization_done = False
        while True:
            for amplifier, phase in zip(self.amplifiers, phase_setting):
                if amplifier.amplifier_name == "A" and not has_a_amplifier_initialized:
                    amplifier.intcode_computer.input_values = phase
                    amplifier.intcode_computer.input_values = 0
                    has_a_amplifier_initialized = True
                else:
                    if is_phase_initialization_done:
                        amplifier.intcode_computer.input_values = output
                    else:
                        amplifier.intcode_computer.input_values = phase
                        amplifier.intcode_computer.input_values = output
                amplifier.intcode_computer.interpret()
                amplifier.intcode_computer.reset_halt_flag()
                output = amplifier.intcode_computer.output
            if self.has_all_amplifiers_halted():
                break
            is_phase_initialization_done = True
        self.set_max_output(output)
        self.reset_all_amplifiers_memory()

    def has_all_amplifiers_halted(self):
        halted = True
        for amplifier in self.amplifiers:
            if not amplifier.intcode_computer.halted:
                halted = False
        return halted

    def reset_all_amplifiers_memory(self):
        for amplifier in self.amplifiers:
            amplifier.intcode_computer.reset()

    @staticmethod
    def get_all_combinations():
        for seq in permutations(ThrusterOptimizer.phase_setting_options, 5):
            yield list(seq)

    def set_max_output(self, value):
        if value is not None:
            print(self.max_output)
            self.max_output = max(self.max_output, value)


def main():
    optimizer = ThrusterOptimizer()
    optimizer.initialize()
    optimizer.optimize_thrust()
    print(optimizer.max_output)


if __name__ == "__main__":
    sys.exit(main())
