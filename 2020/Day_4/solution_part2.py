#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict

import re
import sys
from typing import Optional, Set

INPUT_FILE = "input.txt"


@dataclass(unsafe_hash=True)
class Passport:
    byr: Optional[str] = None
    iyr: Optional[str] = None
    eyr: Optional[str] = None
    hgt: Optional[str] = None
    hcl: Optional[str] = None
    ecl: Optional[str] = None
    pid: Optional[str] = None
    cid: Optional[str] = None

    def is_valid(self) -> bool:
        for key, value in asdict(self).items():
            if not self.validate(key, value):
                return False
        return True

    @staticmethod
    def validate(key: str, value: str) -> bool:
        if key == "cid":
            return True
        if not value:
            return False
        if key == "byr":
            if value.isdigit() and len(value) == 4 and 1920 <= int(value) <= 2002:
                return True
            return False
        if key == "iyr":
            if value.isdigit() and len(value) == 4 and 2010 <= int(value) <= 2020:
                return True
            return False
        if key == "eyr":
            if value.isdigit() and len(value) == 4 and 2020 <= int(value) <= 2030:
                return True
            return False
        if key == "hgt":
            if "cm" in value:
                if 150 <= int(value.split("cm")[0]) <= 193:
                    return True
            if "in" in value:
                if 59 <= int(value.split("in")[0]) <= 76:
                    return True
            return False
        if key == "hcl":
            hcl_regex = re.compile(r"^#[0-9a-f]{6}$")
            if hcl_regex.match(value):
                return True
            return False
        if key == "ecl":
            if value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
                return True
            return False
        if key == "pid":
            if value.isdigit() and len(value) == 9:
                return True
            return False
        return False


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
