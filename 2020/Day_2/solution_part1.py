#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from dataclasses import dataclass
from typing import List

INPUT_FILE = "input.txt"


@dataclass
class Password:
    policy_low: int
    policy_high: int
    policy_letter: str
    password: str


def parse_inputs() -> List[Password]:
    passwords = []
    password_regex = re.compile(r"^(\d*)-(\d*)\s*(\w):\s*(\w+)")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if match := password_regex.match(line):
                passwords.append(
                    Password(
                        int(match.groups()[0]),
                        int(match.groups()[1]),
                        match.groups()[2],
                        match.groups()[3],
                    )
                )

    return passwords


def analyze_passwords(passwords: List[Password]) -> int:
    print(len(passwords))
    valid_occurrences = 0
    for password in passwords:
        if (
            password.policy_low
            <= list(password.password).count(password.policy_letter)
            <= password.policy_high
        ):
            valid_occurrences += 1
        else:
            print(f"Not valid: {str(password)}")
    return valid_occurrences


def main():
    passwords = parse_inputs()
    print(analyze_passwords(passwords))


if __name__ == "__main__":
    sys.exit(main())
