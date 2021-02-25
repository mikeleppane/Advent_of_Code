#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#from dataclasses import dataclass
from itertools import permutations
import re
import sys
from pprint import PrettyPrinter
from typing import Tuple, List
from operator import add
from math import sqrt

INPUT_FILE = "input.txt"


pp = PrettyPrinter(indent=4)


#@dataclass(eq=True)
class Nanobot:
    def __init__(self,x,y,z,r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.r == other.r

    def __str__(self):
        return f"Nanobot(x={self.x}, y={self.y}, z={self.z}, r={self.r})"

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def find_largest_nanobot(nanobots: List[Nanobot]) -> Nanobot:
    return sorted(nanobots, key=lambda nanobot: nanobot.r, reverse=True)[0]


def find_closest_nanobots(nanobots: List[Nanobot]):
    # largest_nanobot = find_largest_nanobot(nanobots)
    # largest_nanobot_index = nanobots.index(largest_nanobot)
    # nanobots.remove(largest_nanobot)
    r = list()
    nb = Nanobot(x=22072014, y=40746738, z=43994665, r=66978889)
    x, y, z = (nb.x-nb.r, nb.y-nb.r, nb.z-nb.r)
    g = list()
    for nanobot in nanobots:
        if nanobot != nb:
            if (
                manhattan((nanobot.x, nanobot.y, nanobot.z), (nb.x, nb.y, nb.z))
                <= nanobot.r
            ):
                g.append(nanobot)
    min_distance = float("inf")
    t = ""
    for nanobot in g:
        if nanobot != nb:
            distance = sqrt((nanobot.x-nb.x)**2 + (nanobot.y-nb.y)**2 + (nanobot.z-nb.z)**2)
            if distance < min_distance:
                min_distance = min(min_distance, distance)
                t = nanobot
    print(t)
    print(min_distance)

    new_max = 0
    distance_to_origin = float("inf")
    nb = Nanobot(x=22072014, y=40746738, z=43994665, r=66978889)
    x, y, z = (nb.x, nb.y, nb.z)
    counts = list()
    for id in range(1,300000000,10000):
        counts.clear()
        for i in set(permutations([0,0,1 * id,1 * id,1 * id,-1 * id,-1 * id,-1 * id],r=3)):
            x,y,z = list(map(add,(x,y,z),i))
            count = 0
            for nanobot in nanobots:
                if (
                    manhattan((nanobot.x, nanobot.y, nanobot.z), (x,y,z))
                    <= nanobot.r
                ):
                    count += 1
            counts.append(count)
            """
            distance_to_zero = manhattan((x,y,z),(0,0,0))
            if count > new_max:
                new_max = max(new_max, count)
                #if distance_to_zero <= distance_to_origin:
                #    distance_to_origin = distance_to_zero
                print(distance_to_zero)
                print(count)
                print(x,y,z)
                print(id)
                #return
            """
        #print(counts)
        if all((c < 852 for c in counts)):
            print(id)
            print(x,y,z)
            return
        #x -= 1
        #y -= 1
        #z -= 1
        # Nanobot(x=22072014, y=40746738, z=43994665, r=66978889), 851)
    """
    for nanobot in nanobots:
        count = 0
        for other_nanobot in nanobots:
            if nanobot != other_nanobot:
                if manhattan((nanobot.x, nanobot.y, nanobot.z), (other_nanobot.x, other_nanobot.y, other_nanobot.z)) <= other_nanobot.r:
                    count += 1
        r.append((nanobot, count))
    """
    # pp.pprint(sorted(r, key=lambda x: x[1]))


def read_nanobots() -> List[Nanobot]:
    nanobots = list()
    position_regex = re.compile(
        r"pos=<([-]?\d{1,12}),([-]?\d{1,12}),([-]?\d{1,12})>\, r=(\d{1,12})"
    )
    radius_regex = re.compile(r"\.*r=(\d{1,10})")
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                x, y, z, r = list(map(int, position_regex.match(line).groups()))
                nanobots.append(Nanobot(x=x, y=y, z=z, r=r))
    return nanobots


def main():
    nanobots = read_nanobots()
    #print(manhattan((21068032,39742756,42990683),(0,0,0)))
    find_closest_nanobots(nanobots)


if __name__ == "__main__":
    sys.exit(main())
