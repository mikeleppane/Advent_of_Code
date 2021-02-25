#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#from dataclasses import dataclass
import re
import sys
from typing import List, Set, Tuple, NamedTuple

INPUT_FILE = "input.txt"


class Claim(NamedTuple):
    ID: int
    from_left_edge: int
    from_top_edge: int
    wide: int
    tall: int


def get_claim_coordinates(claim: Claim) -> Set[Tuple[int]]:
    coordinates = set()
    for x in range(claim.wide):
        for y in range(claim.tall):
            coordinates.add((claim.from_left_edge + x, claim.from_top_edge + y))
    return coordinates


def calculate_same_claims(claims: List[Claim]):
    common_inches = set()
    for claim in claims:
        claim_coordinates = get_claim_coordinates(claim)
        for other_claim in claims:
            if claim.ID != other_claim.ID:
                common = claim_coordinates.intersection(
                    get_claim_coordinates(other_claim)
                )
                if common:
                    for coordinate in common:
                        common_inches.add(coordinate)
    print(len(common_inches))


def read_claims() -> List[Claim]:
    claims = []
    claim_regex = re.compile(
        r"#(\d{1,4})\s@\s(\d{1,3}),(\d{1,3}):\s(\d{1,3})x(\d{1,3})"
    )
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            if line:
                matches = claim_regex.match(line.rstrip()).groups()
                if len(matches) == 5:
                    claim = Claim(
                        ID=int(matches[0]),
                        from_left_edge=int(matches[1]),
                        from_top_edge=int(matches[2]),
                        wide=int(matches[3]),
                        tall=int(matches[4]),
                    )
                    claims.append(claim)
                else:
                    raise ValueError(f"Incorrect claim found: {claim}: {matches}")

    return claims


def main():
    claims = read_claims()
    calculate_same_claims(claims)


if __name__ == "__main__":
    sys.exit(main())
