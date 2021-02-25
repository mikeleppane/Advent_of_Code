#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass

import re
import sys
from pprint import PrettyPrinter
from typing import List, Optional
from itertools import chain
from math import floor
from copy import deepcopy

INPUT_FILE = "input.txt"

pp = PrettyPrinter(indent=4)


@dataclass(eq=True, unsafe_hash=True)
class Group:
    ID: int
    units: int
    hit_points: int
    attack_type: str
    attack_damage: int
    initiative: int
    weaknesses: List[str]
    immunities: List[str]
    group_type: str
    target: Optional["Group"] = None
    damage_factor: int = 1

    @property
    def effective_power(self):
        return self.units * self.attack_damage

    @property
    def is_alive(self):
        return self.units > 0

    def reset(self):
        self.target = None
        self.damage_factor = 1

    def attack(self):
        if self.target:
            left_units = self.target.units - floor(
                (self.damage_factor * self.effective_power) / self.target.hit_points
            )
            if left_units < 0:
                self.target.units = 0
            else:
                self.target.units = left_units


class Immune:
    def __init__(self):
        pass


class Infection:
    def __init__(self):
        pass


def target_selection(groups: List[Group], targets: List[Group]):
    group_targets = []
    for group in groups:
        possible_targets = list()
        if not group.is_alive:
            continue
        for target_group in targets:
            if target_group.ID in group_targets or not target_group.is_alive:
                continue
            if group.attack_type not in target_group.immunities:
                if group.attack_type in target_group.weaknesses:
                    damage = (
                        group.effective_power * 2,
                        target_group,
                        2,
                    )
                    possible_targets.append(damage)
                else:
                    damage = (
                        group.effective_power,
                        target_group,
                        1,
                    )
                    possible_targets.append(damage)
        if possible_targets:
            if len(possible_targets) == 1:
                target = possible_targets[0][1]
                group.target = target
                group.damage_factor = possible_targets[0][2]
                group_targets.append(target.ID)
            else:
                options = list()
                damage_level = sorted(possible_targets, key=lambda item: item[0], reverse=True)[0][0]
                for possible_target in possible_targets:
                    if possible_target[0] == damage_level:
                        options.append(possible_target)
                target_option = sorted(
                    options,
                    key=lambda item: (item[1].effective_power, item[1].initiative),
                    reverse=True,
                )[0]
                group.target = target_option[1]
                group.damage_factor = target_option[2]
                group_targets.append(group.target.ID)
        else:
            group.target = None


def start_fight():
    boost_range = range(37, 501)
    orig_immunes, orig_infections = read_inputs()
    for boost_value in boost_range:
        #for group in chain(immunes, infections):
        #    group.reset()
        immunes = deepcopy(orig_immunes)
        infections = deepcopy(orig_infections)
        for immune_group in immunes:
            immune_group.attack_damage += boost_value
        while True:
            immunes = sorted(
                immunes, key=lambda item: (item.effective_power, item.initiative), reverse=True
            )
            infections = sorted(
                infections,
                key=lambda item: (item.effective_power, item.initiative),
                reverse=True,
            )
            target_selection(immunes, infections)
            target_selection(infections, immunes)


            for group in sorted(
                chain(immunes, infections), key=lambda item: item.initiative, reverse=True
            ):
                if group.is_alive:
                    group.attack()

            if all((group.units == 0 for group in immunes)):
                break
            elif all((group.units == 0 for group in infections)):
                print(f"BOOST value: {boost_value}")
                print(sum(group.units for group in immunes))
                return

            for group in chain(immunes, infections):
                group.reset()
        print(boost_value)



def form_group(group, index, group_type) -> Group:
    units_regex = re.compile(r"(\d{1,5}) units")
    hit_points_regex = re.compile(r"(\d{1,5}) hit points")
    damage_regex = re.compile(r"(\d{1,5}) (\w+) damage")
    initiative_regex = re.compile(r"initiative (\d{1,5})")
    units = int(units_regex.search(group).groups()[0])
    hit_points = int(hit_points_regex.search(group).groups()[0])
    attack_damage, attack_type = damage_regex.search(group).groups()[:]
    initiative = int(initiative_regex.search(group).groups()[0])
    wis = group[group.find("(") + 1 : group.find(")")].split(";")
    weaknesses = list()
    immunities = list()
    for wi in wis:
        if "weak" in wi:
            weaknesses = list(map(str.strip, wi.split("weak to ")[1].split(",")))
        if "immune" in wi:
            immunities = list(map(str.strip, wi.split("immune to ")[1].split(",")))
    return Group(
        ID=index,
        units=units,
        hit_points=hit_points,
        attack_damage=int(attack_damage),
        attack_type=attack_type,
        initiative=initiative,
        weaknesses=weaknesses,
        immunities=immunities,
        group_type=group_type,
    )


def read_inputs():
    immunes = list()
    infections = list()
    with open(INPUT_FILE, "r") as f_handle:
        immune_groups, infection_groups = f_handle.read().split("\n\n")
        immune_groups = immune_groups.split("\n")[1:]
        infection_groups = infection_groups.split("\n")[1:]
        for index, (immune_group, infection_group) in enumerate(
            zip(immune_groups, infection_groups), start=1
        ):
            immunes.append(form_group(immune_group, index, group_type="immune"))
            infections.append(
                form_group(infection_group, index, group_type="infection")
            )
    return immunes, infections


def main():
    start_fight()


if __name__ == "__main__":
    sys.exit(main())
