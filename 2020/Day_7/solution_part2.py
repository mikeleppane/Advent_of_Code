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


dd = Counter()
factors = list()


def contains_bag(bags: List[Bag], main_bag, P, ff):
    print(main_bag.name)
    for bag in bags:
        if bag.name == main_bag.name:
            if len(bag.contains) == 1 and bag.contains[0].count == 0:
                return
            for inside_bag in bag.contains:
                if not inside_bag.name:
                    continue
                if inside_bag.count > 0:
                    dd[P].append(ff * inside_bag.count)
                    contains_bag(bags=bags, main_bag=inside_bag, P=P, ff=dd[P][-1])
    return


def find(bags: List[Bag]):
    for bag in bags:
        if bag.name == "shiny gold":
            for inside_bag in bag.contains:
                factors.append(inside_bag.count)
                dd[inside_bag.name] = list([inside_bag.count])
                contains_bag(bags=bags, main_bag=inside_bag, P=inside_bag.name, ff=inside_bag.count)
                factors.clear()
    print(dd)


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
