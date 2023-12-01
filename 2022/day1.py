import lib

use_example = True
input_text = lib.read_input(__file__, use_example)

"""
# Girts solution

elves = input_text.split("\n\n")
elves2 = sorted(sum(int(cal) for cal in elf.splitlines()) for elf in elves)
print(sum(elves2[-3:]))
"""

cal_list = input_text.splitlines()

elf_cal = 0
# Part 1
#num_elves = 1

# Part 2
num_elves = 3
all_cals = []


for i in cal_list:
    if i:
        elf_cal += int(i)
    else:
        all_cals.append(elf_cal)
        elf_cal = 0

all_cals.sort(reverse=True)

print(sum(all_cals[:num_elves]))
