#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from functools import lru_cache, cache
import sys
from typing import List, Deque

INPUT_FILE = "input.txt"
visited_routes = set()
current_route = set()
DP = {}



def read_adapter_ratings() -> List[int]:
    adapter_ratings = list()
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                try:
                    adapter_ratings.append(int(line.rstrip()))
                except ValueError as ex:
                    print(f"Cannot convert input value {line.rstrip()} to a int type")
                    raise ValueError from ex
    return adapter_ratings


def main():
    def dp(i):
        if i == len(xs) - 1:
            return 1
        if i in DP:
            return DP[i]
        ans = 0
        for j in range(i + 1, len(xs)):
            if xs[j] - xs[i] <= 3:
                ans += dp(j)
        DP[i] = ans
        return ans
    xs = read_adapter_ratings()
    xs.append(0)
    xs.append(max(xs) + 3)
    xs.sort()
    print(xs)
    print(dp(0))
    print(DP)


if __name__ == "__main__":
    sys.exit(main())
