def process_input(input_text, steps):
    stone_line = [int(x) for x in input_text.split()]

    cache: dict[(int, int):int] = {}
    count = 0
    for n in stone_line:
        calculate_stone_count(n, steps, cache)
        count += cache[(n, steps)]

    return count


def calculate_stone_count(val, step, cache):
    #print(f"{"\t"*step}Calculating for {val=}, {step=}")
    score = 0
    if result := cache.get((val, step)):
        #print(f"{"\t"*step}Cache hit: {result=}")
        return result

    if step == 0:
        #print(f"{"\t"*step}Step was zero, return 1")
        score = 1

    # If neither of the base cases, apply the problem ruleset to this number
    else:
        new_vals = apply_rules(val)
        score = 0
        for v in new_vals:
            score += calculate_stone_count(v, step - 1, cache)

    cache[(val, step)] = score
    #print(f"{"\t"*step}Final count: {score=}")
    return score


def apply_rules(val):
    if val == 0:
        return [1]

    str_val = str(val)
    val_len = len(str_val)
    if val_len % 2 == 0:
        num1 = int(str_val[: val_len // 2])
        num2 = int(str_val[(val_len // 2) :])
        return [num1, num2]

    return [val * 2024]


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    input_text = lib.read_input(__file__, use_example)
    steps = 25
    if not part1:
        steps = 75

    return process_input(input_text, steps)


if __name__ == "__main__":
    print(main(part1=False, use_example=False))
