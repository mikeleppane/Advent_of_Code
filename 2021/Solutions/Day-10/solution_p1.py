#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pprint import PrettyPrinter
from typing import List

custom_printer = PrettyPrinter(
    indent=4,
    width=100,
    depth=2,
    compact=True,
    sort_dicts=False,
    underscore_numbers=True,
)

INPUT_FILE = "input.txt"

LEFT_CHUNK_PAIRS = {"(": ")",
                    "[": "]",
                    "{": "}",
                    "<": ">"}
RIGHT_CHUNK_PAIRS = {")": "(",
                     "]": "[",
                     "}": "{",
                     ">": "<"}

SYNTAX_ERROR_SCORES = {")": 3,
                       "]": 57,
                       "}": 1197,
                       ">": 25137}


def read_chunks() -> List[List[str]]:
    chunks: List[List[str]] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                chunks.append(list(line))
    return chunks


def parse_chunk(chunk: List[str], syntax_errors: List[str]):
    corrupted = False
    incomplete = False
    last_char_eaten = ""
    while True:
        for index, char in enumerate(chunk):
            if index == len(chunk) - 1 and char in LEFT_CHUNK_PAIRS:
                incomplete = True
                break
            if char in LEFT_CHUNK_PAIRS:
                last_char_eaten = char
                continue
            if char in RIGHT_CHUNK_PAIRS and RIGHT_CHUNK_PAIRS[char] == last_char_eaten:
                chunk.pop(index)
                chunk.pop(index - 1)
                break
            corrupted = True
            syntax_errors.append(char)
            break
        if incomplete or corrupted or not chunk:
            break


def solve() -> int:
    chunks = read_chunks()
    syntax_errors: List[str] = []
    for chunk in chunks:
        parse_chunk(chunk, syntax_errors)
    return sum([SYNTAX_ERROR_SCORES[error] for error in syntax_errors])


def main() -> None:
    score = solve()
    print(f"Result: {score}")


if __name__ == "__main__":
    sys.exit(main())
