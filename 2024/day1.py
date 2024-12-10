#!/usr/bin/env python3

import collections

import lib


def process_input(input):
    # Create two lists from the input
    list_a = []
    list_b = []
    for line in input.splitlines():
        n = line.split()
        list_a.append(int(n[0]))
        list_b.append(int(n[1]))


    if part1:
        return calculate_list_distance(list_a, list_b)
    else:
        return calculate_similarity_score(list_a, list_b)


def calculate_list_distance(list_a, list_b):
    list_dist = 0
    for a, b in zip(sorted(list_a), sorted(list_b)):
        list_dist += abs(a - b)
    return list_dist

def calculate_similarity_score(list_a, list_b):
    counts = collections.defaultdict(int)
    for b in list_b:
        counts[b] += 1

    sim_score = 0
    for i in list_a:
        sim_score += i * counts[i]
    return sim_score

########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part1 = False
use_example = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)

    answer = process_input(input_text)
    print(answer)
