#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
from typing import List

INPUT_FILE = "input.txt"


class OrbitObject:
    def __init__(self, name, orbits_around):
        self.name = name
        self.orbits_around = orbits_around

    def __str__(self):
        return f"{self.name} orbits directly around {self.orbits_around}"


class OrbitMap:
    total_number_of_orbits = 0
    map: List[OrbitObject] = list()
    COM = "COM"

    def read_orbit_map(self):
        with open(INPUT_FILE, "r") as f_handle:
            for line in f_handle:
                if line:
                    data = line.rstrip().split(")")
                    self.map.append(OrbitObject(name=data[0], orbits_around=data[1]))

    def calculate_total_number_of_orbits(self):
        for orbit in self.map:
            self.total_number_of_orbits += 1
            if orbit.name != self.COM:
                self.find_indirect_orbits(orbit.name)

    def find_indirect_orbits(self, orbit_name):
        if orbit_name != self.COM:
            for orbit in self.map:
                if orbit.orbits_around == orbit_name:
                    self.total_number_of_orbits += 1
                    self.find_indirect_orbits(orbit.name)


def main():
    orbit_map = OrbitMap()
    orbit_map.read_orbit_map()
    orbit_map.calculate_total_number_of_orbits()
    print(orbit_map.total_number_of_orbits)


if __name__ == "__main__":
    sys.exit(main())
