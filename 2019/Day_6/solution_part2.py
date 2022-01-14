#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from collections import deque
from typing import Deque, List, NamedTuple

INPUT_FILE = "input.txt"


class OrbitObject:
    def __init__(self, name, orbits_around):
        self.name = name
        self.orbits_around = orbits_around

    def __str__(self):
        return f"{self.orbits_around} orbits directly around {self.name}"

    def __eq__(self, other):
        return self.name == other.name and self.orbits_around == other.orbits_around

    def __hash__(self):
        return hash(str(self))


class TravelObject(NamedTuple):
    name: str
    orbit_object: OrbitObject


class OrbitMap:
    COM, YOU, SAN = ("COM", "YOU", "SAN")

    def __init__(self):
        self.map: List[OrbitObject] = list()

    def read_orbit_map(self):
        with open(INPUT_FILE, "r") as f_handle:
            for line in f_handle:
                if line:
                    data = line.rstrip().split(")")
                    self.map.append(OrbitObject(name=data[0], orbits_around=data[1]))

    def get_starting_point_from_map(self):
        for orbit in self.map:
            if self.is_starting_point(orbit.orbits_around):
                return orbit

    def is_center_of_mass(self, name):
        return name == self.COM

    def is_starting_point(self, name):
        return name == self.YOU

    def is_santa(self, name):
        return name == self.SAN


class Traveller:
    def __init__(self):
        self.orbit_map = OrbitMap()
        self.travelled_path: Deque[TravelObject] = deque()
        self.minimum_distance = float("inf")
        self.non_valid_routes = set()

    def calculate_minimum_orbital_trasfer(self):
        self.orbit_map.read_orbit_map()
        starting_object = self.orbit_map.get_starting_point_from_map()
        self.travelled_path.append(TravelObject(starting_object.name, starting_object))
        self._find_minimum_distance()

    def _find_minimum_distance(self):
        while True:
            latest_visited_item = self._get_last_travelled_item()
            if not latest_visited_item:
                break
            found_path = False
            for orbit in self.orbit_map.map:
                if orbit != latest_visited_item.orbit_object and not self.orbit_map.is_starting_point(orbit.name):
                    if orbit.orbits_around == latest_visited_item.name:
                        if self.orbit_map.is_center_of_mass(orbit.name):
                            continue
                        if (orbit.name, orbit) not in self.non_valid_routes:
                            if self.orbit_map.is_santa(orbit.name):
                                self._set_minimum_distance()
                            self.travelled_path.append(TravelObject(orbit.name, orbit))
                            found_path = True
                            break
                    if orbit.name == latest_visited_item.name:
                        if (orbit.orbits_around, orbit) not in self.non_valid_routes:
                            if self.orbit_map.is_santa(orbit.orbits_around):
                                self._set_minimum_distance()
                            self.travelled_path.append(TravelObject(orbit.orbits_around, orbit))
                            found_path = True
                            break
            if not found_path:
                self._handle_if_not_found_path()

    def _set_minimum_distance(self):
        self.minimum_distance = min(self.minimum_distance, len(self.travelled_path) - 1)

    def _handle_if_not_found_path(self):
        if self.travelled_path[-1] not in self.non_valid_routes:
            self.non_valid_routes.add(self.travelled_path[-1])
        self.travelled_path.pop()

    def _get_last_travelled_item(self):
        if self.travelled_path:
            return self.travelled_path[-1]
        return ()


def main():
    traveller = Traveller()
    traveller.calculate_minimum_orbital_trasfer()
    print(f"Minimum orbital path from YOU to SAN is: {traveller.minimum_distance}")


if __name__ == "__main__":
    sys.exit(main())
