import collections


def process_input(input, part1):
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
    ### Jenny's original
    # list_a.sort()
    # list_b.sort()
    # list_dist = 0
    # for i in range(len(list_a)):
    #     list_dist += abs(int(list_a[i]) - int(list_b[i]))

    ### Girts' contribution
    for a, b in zip(sorted(list_a), sorted(list_b)):
        list_dist += abs(a - b)

    return list_dist


def calculate_similarity_score(list_a, list_b):
    sim_score = 0
    ### Jenny's original
    # # Can make this smarter using a dictionary or somesuch, so I'm not counting duplicate numbers multiple times.
    # for i in list_a:
    #     b_count = list_b.count(i)
    #     sim_score += int(i) * int(b_count)

    ### Girts' contribution

    counts = collections.defaultdict(int)
    for b in list_b:
        counts[b] += 1
    for i in list_a:
        sim_score += i * counts[i]
    return sim_score


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=True, use_example=False))
