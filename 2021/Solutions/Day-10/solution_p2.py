#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from math import floor
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

LEFT_CHUNK_PAIRS = {"(": ")", "[": "]", "{": "}", "<": ">"}
RIGHT_CHUNK_PAIRS = {")": "(", "]": "[", "}": "{", ">": "<"}

POINTS = {")": 1, "]": 2, "}": 3, ">": 4}


def read_chunks() -> List[List[str]]:
    chunks: List[List[str]] = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                chunks.append(list(line))
    return chunks


def find_closing_chars_for_incomplete_chunks(
        chunk: List[str], closing_chars_for_incomplete_chunks: List[List[str]]
):
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
            break
        if corrupted or not chunk:
            break
        if incomplete:
            closing_chars_for_incomplete_chunks.append(
                [LEFT_CHUNK_PAIRS[char] for char in reversed(chunk)]
            )
            break


def find_middle_score(chunks: List[List[str]]):
    scores: List[int] = []
    for chunk in chunks:
        total_score = 0
        for char in chunk:
            total_score = total_score * 5 + POINTS[char]
        scores.append(total_score)
    return sorted(scores)[floor(len(scores) // 2)]


def solve():
    chunks = read_chunks()
    closing_chars_for_incomplete_chunks: List[List[str]] = []
    for chunk in chunks:
        find_closing_chars_for_incomplete_chunks(
            chunk, closing_chars_for_incomplete_chunks
        )

    return find_middle_score(closing_chars_for_incomplete_chunks)


def main():
    score = solve()
    print(f"Result: {score}")


if __name__ == "__main__":
    sys.exit(main())
