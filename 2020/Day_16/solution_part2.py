#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from math import prod
import re
import sys
from typing import Dict, Tuple, List, Iterator

INPUT_FILE = "input.txt"


@dataclass
class Rule:
    rules: Dict[str, List[Iterator]]


@dataclass(eq=True)
class Tickets:
    my_ticket: List[int]
    nearby_tickets: List[List[int]]


def find_correct_fields(rule: Rule, tickets: Tickets) -> Dict[str, List[int]]:
    field_names: Dict[str, List[int]] = dict()
    for field_index in range(len(tickets.nearby_tickets[0])):
        for rule_name, rules in rule.rules.items():
            is_valid = True
            for ticket in tickets.nearby_tickets:
                if not (
                    ticket[field_index] in rules[0] or ticket[field_index] in rules[1]
                ):
                    is_valid = False
                    break
            if is_valid:
                if rule_name in field_names:
                    field_names[rule_name].append(field_index)
                else:
                    field_names.update({rule_name: [field_index]})

    while True:
        unique_indexes = list()
        for name, index in field_names.items():
            if len(index) == 1:
                unique_indexes.append(index[0])
        for index in sorted(unique_indexes, reverse=True):
            for indexes in field_names.values():
                if len(indexes) == 1:
                    continue
                if index in indexes:
                    indexes.remove(index)
        if all([len(indexes) == 1 for indexes in field_names.values()]):
            break
    return field_names


def remove_invalid_tickets(rule: Rule, tickets: Tickets) -> None:
    invalid_tickets = set()
    for index, ticket in enumerate(tickets.nearby_tickets):
        for field in ticket:
            is_valid = False
            for rules in rule.rules.values():
                if field in rules[0] or field in rules[1]:
                    is_valid = True
            if not is_valid:
                invalid_tickets.add(index)

    for index in sorted(invalid_tickets, reverse=True):
        tickets.nearby_tickets.pop(index)


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
    remove_invalid_tickets(rule=ticket_rules, tickets=tickets)
    fields = find_correct_fields(rule=ticket_rules, tickets=tickets)
    print(fields)
    print(
        prod(
            [
                tickets.my_ticket[index[0]]
                for name, index in fields.items()
                if "departure" in name
            ]
        )
    )


if __name__ == "__main__":
    sys.exit(main())
