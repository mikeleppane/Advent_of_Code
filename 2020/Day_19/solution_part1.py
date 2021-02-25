#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import sys
import re
from boltons.iterutils import flatten
from typing import List, TypedDict, Dict, Union, Tuple

INPUT_FILE = "input.txt"


class Rules(TypedDict):
    rule: List[str]


def compose_regex_from_rule(rules: Dict[int, Union[List[str], str]]) -> str:
    rule_regex = list()
    for rule in rules[0]:
        rule_regex.append(rule)
    while True:
        for index, rule in enumerate(rule_regex):
            if rule not in ("|", "(" ")") and rule.isdigit():
                rule_value = rules[int(rule)]
                if isinstance(rule_value, str):
                    rule_regex[index] = rule_value
                if isinstance(rule_value, list):
                    rule_with_parenthesis = ["(", ")"]
                    rule_with_parenthesis.insert(1, rules[int(rule)])
                    rule_regex[index] = rule_with_parenthesis
        rule_regex = flatten(rule_regex)
        if any([rule.isdigit() for rule in rule_regex]):
            continue
        else:
            break
    return r"^(" + "".join(rule_regex) + ")$"


def find_messages_that_match_rule_0(
    rules: Dict[int, Union[List[str], str]], messages: List[str] = None
):
    rule_regex = re.compile(compose_regex_from_rule(rules))
    print(rule_regex)
    count = 0
    for message in messages:
        result = rule_regex.findall(message)
        if result and message in result[0]:
            count += 1
    print(count)


def read_rules_and_messages() -> Tuple[Dict[int, Union[List[str], str]], List[str]]:
    rules = dict()
    messages = list()
    read_messages = False
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                if read_messages:
                    messages.append(line)
                    continue
                else:
                    rule, rule_values = line.split(":")
                    if '"' in rule_values:
                        rules.update({int(rule): rule_values.lstrip().split('"')[1]})
                    else:
                        rules.update({int(rule): rule_values.lstrip().split(" ")})
            else:
                read_messages = True
    return rules, messages


def main():
    rules, messages = read_rules_and_messages()
    find_messages_that_match_rule_0(rules, messages)


if __name__ == "__main__":
    sys.exit(main())
