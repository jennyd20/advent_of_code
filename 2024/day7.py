def process_input(input):
    total_calibration_result = 0
    for eq in input.splitlines():
        total_calibration_result += get_calibration_result(eq)
    return total_calibration_result


def get_calibration_result(eq):
    # A line represents an equation - test value is before the colon, equation numbers after
    eq_split = eq.split(": ")
    val = int(eq_split[0])
    nums = [int(x) for x in eq_split[1].split(" ")]

    if can_make_equation(val, nums[1:], nums[0]):
        return val
    else:
        return 0


def can_make_equation(val, nums, total):
    # Base case - if we've checked all the numbers in this equation, check for match and return
    if not nums:
        return total == val

    # Pruning case - if the value is already too big, return
    if total > val:
        return False

    # Recursive case - check both the addition and multiplicative cases.
    new_operand, *rest = nums
    result = (can_make_equation(val, rest, total * new_operand)) or (
        can_make_equation(val, rest, total + new_operand)
    )
    if part1:
        return result
    # Part 2 - check when the current total is concatenated with the next value in the list of operands
    return result or can_make_equation(val, rest, concat_nums(total, new_operand))


def concat_nums(a, b):
    result = int(str(a) + str(b))
    return result


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
part1 = False
use_example = False

# Execute the script
from aoc_libs import lib

if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)
    answer = process_input(input_text)
    print(answer)
