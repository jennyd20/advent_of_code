import re


def process_input(input):
    total = 0

    valid_muls_re = r"mul\((\d{1,3}),(\d{1,3})\)"

    # If in part 2, remove all the dont()->do() sections from the string
    if part2:
        # (?s) -> make dot matches all, including newlines
        # Because of how the examples are set up, match both "don't" and "do_not_mul"
        strip_donts_re = r"(?s)(?:don't|do_not_mul\(\)).*?do\(\)"
        new_input = re.sub(strip_donts_re, "", input)
        input = new_input

    for operands in re.findall(valid_muls_re, input):
        total += int(operands[0]) * int(operands[1])
    return total


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part2 = True

# Execute the script
from aoc_libs import lib

if __name__ == "__main__":
    use_example = False
    # day3_2_ex = "day3_2_ex.txt"
    input_text = lib.read_input(__file__, use_example)
    # input_text = lib.read_input(__file__, alt_input=day3_2_ex)

    answer = process_input(input_text)
    print(answer)
