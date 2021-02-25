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


def sub_game(deck_1, deck_2):
    deck_1 = deque(deck_1)
    deck_2 = deque(deck_2)
    player_1_previous_rounds = list()
    player_2_previous_rounds = list()
    while deck_1 and deck_2:
        winner = 0
        player_1_previous_rounds.append(deque(deck_1))
        player_2_previous_rounds.append(deque(deck_2))

        player_1_card = deck_1.popleft()
        player_2_card = deck_2.popleft()

        if len(deck_1) >= player_1_card and len(deck_2) >= player_2_card:
            winner = sub_game(list(deck_1)[:player_1_card], list(deck_2)[:player_2_card])

        if winner != 0:
            if winner == 1:
                deck_1.append(player_1_card)
                deck_1.append(player_2_card)
            else:
                deck_2.append(player_2_card)
                deck_2.append(player_1_card)
        else:
            if player_1_card > player_2_card:
                deck_1.append(player_1_card)
                deck_1.append(player_2_card)
            elif player_2_card > player_1_card:
                deck_2.append(player_2_card)
                deck_2.append(player_1_card)
        for deck_11, deck_22 in zip(player_1_previous_rounds, player_2_previous_rounds):
            if deck_1 == deck_11 or deck_2 == deck_22:
                return 1

    if deck_1:
        return 1
    else:
        return 2


def calculate_winners_score(deck: Deque[int]) -> int:
    score = 0
    for factor in range(1, len(deck) + 1):
        score += factor * deck.pop()
    return score


def play_game(players: List[Player]):
    player_1: Player = players[0]
    player_2: Player = players[1]
    player_1_previous_rounds = list()
    player_2_previous_rounds = list()
    # previous_rounds.append(deque(player_1.deck))
    # previous_rounds.append(deque(player_2.deck))
    while player_1.deck and player_2.deck:
        winner = 0
        player_1_previous_rounds.append(deque(player_1.deck))
        player_2_previous_rounds.append(deque(player_2.deck))

        player_1_card = player_1.deck.popleft()
        player_2_card = player_2.deck.popleft()

        if len(player_1.deck) >= player_1_card and len(player_2.deck) >= player_2_card:
            winner = sub_game(list(player_1.deck)[:player_1_card], list(player_2.deck)[:player_2_card])

        if winner != 0:
            if winner == 1:
                player_1.deck.append(player_1_card)
                player_1.deck.append(player_2_card)
            else:
                player_2.deck.append(player_2_card)
                player_2.deck.append(player_1_card)
        else:
            if player_1_card > player_2_card:
                player_1.deck.append(player_1_card)
                player_1.deck.append(player_2_card)
            elif player_2_card > player_1_card:
                player_2.deck.append(player_2_card)
                player_2.deck.append(player_1_card)
        for deck_1, deck_2 in zip(player_1_previous_rounds, player_2_previous_rounds):
            if deck_1 == player_1.deck or deck_2 == player_2.deck:
                print("sdfsd")
                print(calculate_winners_score(player_1.deck))
                return


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
