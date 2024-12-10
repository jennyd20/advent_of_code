#!/usr/bin/env python3


def process_input(input, part2):
    # Create list of reports (each input line is a report)
    # Each report is a list of numbers
    reports_list = []
    for report_in in input.split("\n"):
        num_list = [int(x) for x in report_in.split(" ")]
        reports_list.append(num_list)

    safe_count = 0
    for r in reports_list:
        if (part2 and is_safe_part2(r)) or (not part2 and is_safe(r)):
            safe_count += 1
    return safe_count


def is_safe_part2(report):
    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1:]):
            return True
    return False


def is_safe(report):
    inc = None
    lev_1 = report[0]

    for lev_2 in report[1:]:
        # Compare this level with the prior one
        diff = lev_2 - lev_1

        # If the level has changed too much, automatically fail
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        # If necessary, initialize inc boolean value
        if inc is None:
            inc = diff > 0

        # If we aren't following the prior pattern, fail
        if (inc and diff < 0) or (not inc and diff > 0):
            return False

        # Increment the lev_1 counter for the next set of comparisons
        # Note, only if we didn't find a failure at this pass
        lev_1 = lev_2

    # The report has met the safety conditions for all levels
    return True


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
import lib

part2 = True
use_example = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)

    answer = process_input(input_text, part2)
    print(answer)
