#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from collections import Counter
import re
import sys
from typing import List, NamedTuple

INPUT_FILE = "input.txt"


class InsideBag(NamedTuple):
    name: str
    count: int


@dataclass(unsafe_hash=True, eq=True)
class Bag:
    name: str
    contains: List[InsideBag]


def contains_bag(bags: List[Bag], search_bag, main_bag):
    for bag in bags:
        if bag.name == main_bag or not main_bag:
            if bag.name != search_bag:
                for inside_bag in bag.contains:
                    if not inside_bag.name:
                        continue
                    if inside_bag.name == search_bag:
                        return True
                    k = contains_bag(
                        bags=bags, search_bag=search_bag, main_bag=inside_bag.name
                    )
                    if k:
                        return True
                    else:
                        continue
    return False


def find(bags: List[Bag]):
    count = 0
    for bag in bags:
        if contains_bag(bags=bags, search_bag="shiny gold", main_bag=bag.name):
            count += 1
    print(count)


def read_bags() -> List[Bag]:
    bags = list()
    main_bag_regex = re.compile(r"^([\w\s]*)\sbags")
    other_bag_regex = re.compile(r"^(\d+)\s([\w\s]*)\sbag")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                bag = Bag(name="", contains=list())
                main_bag, inside_bags = line.rstrip().rstrip(".").split("contain")
                if match := main_bag_regex.match(main_bag.strip()):
                    bag.name = match.groups()[0]
                for inside_bag in inside_bags.split(","):
                    bag_info = other_bag_regex.match(inside_bag.strip())
                    if not bag_info:
                        bag.contains.append(InsideBag(name="", count=0))
                    else:
                        count, name = bag_info.groups()
                        bag.contains.append(InsideBag(name=name, count=int(count)))
                bags.append(bag)
    return bags


def main():
    bags = read_bags()
    find(bags)


if __name__ == "__main__":
    sys.exit(main())
