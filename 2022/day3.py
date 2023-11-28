import lib

use_example = False
input_text = lib.read_input(__file__, use_example)

import string

# Create the dictionary of letters (for priority of items in the rucksacks)
# Position in the list is equivalent to the priority (modulo 1)
pri_val_list = string.ascii_lowercase + string.ascii_uppercase


# Input is a list of strings
# Find the duplicate character between all the sets
# Compare the first list with the next list in the sets, then recursively return the new duplicate set with the remaining lists to check
def find_dup(input_sets):
    if len(input_sets) == 1:
        return input_sets
    else:
        first_set = input_sets.pop(0)
        comparison_set = input_sets.pop(0)
        dup_items = ""
        for i in first_set:
            if i in comparison_set and i not in dup_items:
                dup_items += i

    input_sets.append(dup_items)
    return find_dup(input_sets)


# Split a rucksack string into two equal lists
def split_rucksack(rucksack):
    rs_compartment_len = len(rucksack) // 2
    rs_l = rucksack[:rs_compartment_len]
    rs_r = rucksack[rs_compartment_len:]

    return [rs_l, rs_r]


# Return the priority of an item based on its position in the dictionary
def get_priority(dup):
    # There should only be one dup at this point
    pri = pri_val_list.index(dup[0]) + 1
    return pri


rucksacks = input_text.splitlines()

# Part 1
# answer = sum(get_priority(find_dup(split_rucksack(rucksack))) for rucksack in rucksacks)


# Part 2
elf_sets_of_three = lib.split_list(rucksacks, 3)
answer = sum(get_priority(find_dup(elf_set)) for elf_set in elf_sets_of_three)

print(("*** USING EXAMPLE ***: " if use_example else "") + str(answer))
