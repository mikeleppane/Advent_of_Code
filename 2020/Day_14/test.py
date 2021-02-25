#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from itertools import product


def main():
    t = set()
    i = 0
    for index in product('000000000111111111', repeat=9):
        i += 1
        if index not in t:
            t.add(index)
            print(i)


if __name__ == "__main__":
    sys.exit(main())
