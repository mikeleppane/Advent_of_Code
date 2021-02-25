#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import deque

import sys
from typing import List

INPUT_FILE = "input.txt"


def play_marble_game(number_of_players=10):
    position = 0
    starting_marble = 0
    game_board = deque((starting_marble,))
    players = {player_index: 0 for player_index in range(1, number_of_players + 1)}
    marble_count = 1
    while True:
        for player_index in range(1, number_of_players + 1):
            if len(game_board) == 1:
                game_board.append(marble_count)
                position = 1
            else:
                if marble_count % 23 == 0:
                    players[player_index] += marble_count
                    current_pos = position
                    game_board.rotate(-current_pos + 7)
                    f = game_board.popleft()
                    players[player_index] += f
                    current_marble = game_board.popleft()
                    game_board.appendleft(current_marble)
                    game_board.rotate(current_pos)
                    g = list(game_board)
                    g = g[0:g.index(current_marble)+1]
                    #game_board = deque(g)
                    game_board = deque(g)
                else:
                    current_pos = position
                    game_board.rotate(-current_pos)
                    game_board.insert(2, marble_count)
                    position = position + 2
                    game_board.rotate(current_pos)

            if marble_count == 1618:
                return max(players.values())
            marble_count += 1


def read_inputs() -> List[int]:
    license_file = []
    with open(INPUT_FILE, "r") as f_handle:
        for line in f_handle:
            line = line.rstrip()
            if line:
                license_file = list(map(int, line.split(" ")))

    return license_file


def main():
    # license_file = read_inputs()
    # cProfile.run("play_marble_game()")
   print(play_marble_game())


if __name__ == "__main__":
    sys.exit(main())
