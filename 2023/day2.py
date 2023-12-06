import re
import lib
from functools import reduce
from operator import mul

# For Part 1
max_values = {"red": 12, "green": 13, "blue": 14}


# Create a mapping of cube colors to the number of cubes in a pull of blocks
def create_color_dict(blocks):
    group = blocks.split(",")
    dict = {}
    for pull in group:
        num, color = pull.strip().split(" ")
        dict[color] = int(num)
    return dict


# Part 1
def possible_games(game):
    split_game = game.split(":")
    game_id = int(split_game[0].split(' ')[1])
    blocks_shown = split_game[1].split(";")

    for blocks in blocks_shown:
        dict = create_color_dict(blocks)

        for key, value in max_values.items():
            if dict.get(key, 0) > value:
                return 0

    return game_id


# Part 2
def game_power(game):
    min_values = {"red": 0, "green": 0, "blue": 0}

    split_game = game.split(":")
    blocks_shown = split_game[1].split(";")

    for blocks in blocks_shown:
        dict = create_color_dict(blocks)

        for key, value in min_values.items():
            min_values[key] = max(value, dict.get(key, 0))

    return reduce(mul, min_values.values())


### SCRIPT ARGUMENTS ###
use_example = False

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    # Part 1
    answer = sum(possible_games(game) for game in input_text.splitlines())

    # Part 2
    #answer = sum(game_power(game) for game in input_text.splitlines())
    print(answer)
