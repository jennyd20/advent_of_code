import lib


def process_input(input):
    # Create two lists from the input
    list_a = []
    list_b = []
    for line in input.split("\n"):
        n = line.split()
        list_a.append(n[0])
        list_b.append(n[1])

    if part1:
        return calculate_list_distance(list_a, list_b)
    else:
        return calculate_similarity_score(list_a, list_b)


def calculate_list_distance(list_a, list_b):
    list_a.sort()
    list_b.sort()
    list_dist = 0
    for i in range(len(list_a)):
        list_dist += abs(int(list_a[i]) - int(list_b[i]))
    return list_dist

def calculate_similarity_score(list_a, list_b):
    sim_score = 0
    # Can make this smarter using a dictionary or somesuch, so I'm not counting duplicate numbers multiple times.
    for i in list_a:
        b_count = list_b.count(i)
        sim_score += int(i) * int(b_count)
    return sim_score

########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part1 = False
use_example = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)

    answer = process_input(input_text)
    print(answer)
