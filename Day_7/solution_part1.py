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
            f"input_signal={self.input_signal}"
        )

    def __repr__(self):
        return self.__str__()


class ThrusterOptimizer:
    phase_setting_options = [0, 1, 2, 3, 4]

    def __init__(self):
        self.max_output = 0
        self.amplifiers = list()

    def initialize(self):
        opcodes = read_opcodes()
        for name in ("A", "B", "C", "D", "E"):
            self.amplifiers.append(Amplifier(name=name, amplifier_software=opcodes))

    def optimize_thrust(self):
        for phase_setting in self.get_all_combinations():
            self.process_amplifier_pipeline(phase_setting)

    def process_amplifier_pipeline(self, phase_setting):
        output = 0
        for amplifier, phase in zip(self.amplifiers, phase_setting):
            if amplifier.amplifier_name == "A":
                amplifier.intcode_computer.input_values = phase
                amplifier.intcode_computer.input_values = 0
            else:
                amplifier.intcode_computer.input_values = phase
                amplifier.intcode_computer.input_values = output
            amplifier.intcode_computer.interpret()
            output = amplifier.intcode_computer.output
            amplifier.intcode_computer.reset()
        self.set_max_output(output)

    def get_all_combinations(self):
        for seq in permutations(ThrusterOptimizer.phase_setting_options, 5):
            yield seq

    def set_max_output(self, value):
        if value is not None:
            self.max_output = max(self.max_output, value)


def main():
    optimizer = ThrusterOptimizer()
    optimizer.initialize()
    optimizer.optimize_thrust()
    print(optimizer.max_output)


if __name__ == "__main__":
    sys.exit(main())
