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
    password_regex = re.compile(r"^(\d+)-(\d+)\s*(\w):\s*(\w+)")
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
    valid_occurrences = 0
    for password in passwords:
        if is_password_valid(password):
            valid_occurrences += 1
        else:
            print(f"Not valid: {str(password)}")
    return valid_occurrences


def is_password_valid(password: Password) -> bool:
    found = False
    if password.policy_letter in password.password:
        try:
            if (
                password.password[password.policy_low - 1] == password.policy_letter
                and not password.password[password.policy_high - 1]
                == password.policy_letter
            ):
                found = True
            if (
                not password.password[password.policy_low - 1] == password.policy_letter
                and password.password[password.policy_high - 1]
                == password.policy_letter
            ):
                found = True
        except IndexError:
            found = False
    return found


def main():
    passwords = parse_inputs()
    print(f"Found valid passwords: {analyze_passwords(passwords)}")


if __name__ == "__main__":
    sys.exit(main())
