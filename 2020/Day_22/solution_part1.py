#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from dataclasses import dataclass
from enum import Enum

import sys
from typing import NamedTuple, Deque, List

INPUT_FILE = "input.txt"


class Player(NamedTuple):
    x: int
    y: int


@dataclass(eq=True)
class Player:
    name: str
    deck: Deque[int]


def calculate_winners_score(deck: Deque[int]) -> int:
    score = 0
    for factor in range(1, len(deck) + 1):
        score += factor * deck.pop()
    return score


def play_game(players: List[Player]):
    player_1: Player = players[0]
    player_2: Player = players[1]
    while player_1.deck and player_2.deck:
        player_1_card = player_1.deck.popleft()
        player_2_card = player_2.deck.popleft()
        if player_1_card > player_2_card:
            player_1.deck.append(player_1_card)
            player_1.deck.append(player_2_card)
        else:
            player_2.deck.append(player_2_card)
            player_2.deck.append(player_1_card)
    if player_1.deck:
        print(calculate_winners_score(player_1.deck))
    else:
        print(calculate_winners_score(player_2.deck))


def read_players() -> List[Player]:
    players = list()
    with open(INPUT_FILE, "r") as f_handle:
        new_player = True
        for line in f_handle:
            line = line.rstrip()
            if line:
                if new_player:
                    player = Player("", deque())
                    new_player = False
                if "player" in line.lower():
                    player.name = line.rstrip(":")
                else:
                    player.deck.append(int(line))
            else:
                new_player = True
                players.append(player)
    players.append(player)

    return players


def main():
    players = read_players()
    play_game(players)


if __name__ == "__main__":
    sys.exit(main())
