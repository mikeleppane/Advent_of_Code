#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from enum import Enum
import re
import sys
from typing import Deque, Dict, Tuple, List, Iterator

INPUT_FILE = "input.txt"
REFERENCE_TILE = (0, 0)

BLACK, WHITE = (0, 1)


class Direction(Enum):
    EAST = "e"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    WEST = "w"
    NORTHWEST = "nw"
    NORTHEAST = "ne"


DIRECTION_SLOPES = {
    "e": (1, 0),
    "se": (0.5, -0.5),
    "sw": (-0.5, -0.5),
    "w": (-1, 0),
    "nw": (-0.5, 0.5),
    "ne": (0.5, 0.5),
}


@dataclass
class Rule:
    rules: Dict[str, List[Iterator]]


@dataclass(eq=True)
class Tickets:
    my_ticket: List[int]
    nearby_tickets: List[List[int]]


def scan_tickets(rule: Rule, tickets: Tickets):
    invalid_fields = list()
    for ticket in tickets.nearby_tickets:
        is_valid = False
        for field in ticket:
            is_valid = False
            for rules in rule.rules.values():
                if field in rules[0] or field in rules[1]:
                    is_valid = True
            if not is_valid:
                invalid_fields.append(field)

    print(sum(invalid_fields))


def read_tickets() -> Tuple[Rule, Tickets]:
    ticket_rules = Rule(rules=dict())
    tickets = Tickets(my_ticket=list(), nearby_tickets=list())
    rule_regex = re.compile(r"([\w\s]+):\s(\d+)-(\d+)\sor\s(\d+)-(\d+)")
    with open(INPUT_FILE, "r") as f_handle:
        lines = f_handle.read().split("\n\n")
        rules = lines[0].split("\n")
        for rule in rules:
            if match := rule_regex.match(rule):
                (
                    rule_name,
                    lower_bound_rule_1,
                    upper_bound_rule_1,
                    lower_bound_rule_2,
                    upper_bound_rule_2,
                ) = match.groups()
                ticket_rules.rules[rule_name] = [
                    range(int(lower_bound_rule_1), int(upper_bound_rule_1) + 1),
                    range(int(lower_bound_rule_2), int(upper_bound_rule_2) + 1),
                ]
        my_ticket = lines[1].split("\n")
        tickets.my_ticket = list(map(int, my_ticket[1].split(",")))
        nearby_tickets = lines[2].split("\n")
        for ticket in nearby_tickets[1:]:
            tickets.nearby_tickets.append(list(map(int, ticket.split(","))))
    return ticket_rules, tickets


def main():
    ticket_rules, tickets = read_tickets()
    scan_tickets(rule=ticket_rules, tickets=tickets)


if __name__ == "__main__":
    sys.exit(main())
