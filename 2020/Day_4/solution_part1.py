#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict

import sys
from typing import Optional, Set

INPUT_FILE = "input.txt"


@dataclass(unsafe_hash=True)
class Passport:
    byr: Optional[int] = None
    iyr: Optional[int] = None
    eyr: Optional[int] = None
    hgt: Optional[str] = None
    hcl: Optional[str] = None
    ecl: Optional[str] = None
    pid: Optional[int] = None
    cid: Optional[int] = None

    def is_valid(self) -> bool:
        valid = True
        for key, value in asdict(self).items():
            if key != "cid" and not value:
                valid = False
        return valid


def read_passports() -> Set[Passport]:
    passports = set()
    with open(INPUT_FILE, "r") as f_handle:
        new_passport = True
        for line in f_handle:
            line = line.rstrip()
            if new_passport:
                passport = Passport()
            if line:
                new_passport = False
                for item in line.split():
                    key, value = item.split(":")
                    setattr(passport, key, value)
            else:
                passports.add(passport)
                new_passport = True
        passports.add(passport)
    return passports


def count_valid_passports(passports: Set[Passport]) -> int:
    valid_passports = 0
    for passport in passports:
        if passport.is_valid():
            valid_passports += 1
    return valid_passports


def main():
    passports = read_passports()
    print(f"Number of valid passports: {count_valid_passports(passports)}")


if __name__ == "__main__":
    sys.exit(main())
