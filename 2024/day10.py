"""
Day10 - https://adventofcode.com/2024/day/10

Goal:
* find paths starting from the lowest height, a trailhead (0)...
* that increase gradually (+1 to neighbor)...
* to the highest point (ends at 9)

"""

from __future__ import annotations
from aoc_libs.grid import Position
from aoc_libs.grid import Grid
import collections


def process_input(input, part1=True):
    # Create an integer map from the input text
    # The integers correspond to the height of that position of the map
    topo_map: Grid[int] = Grid.create_from_input(input, new_type=lambda x: int(x, 16))

    # Solve the problem
    trailmap_scores, trailmap_summits = generate_trailmap(topo_map)

    # Calculate the scores of the trailheads
    trailheads = topo_map.get_all_val_pos(0)
    score = 0
    for t in trailheads:
        if part1:
            score += len(trailmap_summits[t])
        else:
            score += trailmap_scores[t]
    return score


# Create a dictionaries of positions to scores, starting at the end of the trail and working backward
def generate_trailmap(topo_map: Grid):
    # Map positions to a set of positions
    trailmap_scores: dict[Position, int] = {}
    trailmap_summits: dict[Position, set[Position]] = collections.defaultdict(set)

    # Start at the highest point (9) and work down
    trail_height = 9
    while trail_height >= 0:
        # For every position of a given value, find its score
        for p in topo_map.get_all_val_pos(trail_height):
            update_trailmaps(trail_height, p, trailmap_scores, trailmap_summits, topo_map)
        trail_height -= 1

    return trailmap_scores, trailmap_summits


def update_trailmaps(
    trail_height: int,
    initial_pos: Position,
    trailmap_scores: dict[Position, int],
    trailmap_summits: dict[Position, set[Position]],
    topo_map: Grid):
    if trail_height == 9:
        trailmap_scores[initial_pos] = 1
        trailmap_summits[initial_pos] = {initial_pos}
        return

    score = 0
    for next_pos in initial_pos.get_orthog_pos(topo_map):
        if topo_map.get_val(next_pos) == trail_height + 1:
            score += trailmap_scores[next_pos]
            trailmap_summits[initial_pos].update(trailmap_summits[next_pos])
    trailmap_scores[initial_pos] = score


# For a given position, see if any of the orthogonal positions are at the given trail height
def prev_valid_pos(
    start_pos: Position, trail_height: int, topo_map: Grid
) -> set[Position]:
    prev_trails = set()
    for p in start_pos.get_orthog_pos(topo_map):
        if topo_map.get_val(p) == trail_height:
            prev_trails.add(p)
    return prev_trails

########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=False, use_example=False))
