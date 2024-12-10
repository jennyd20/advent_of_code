from numpy import true_divide


def process_input(input, dampener_val=0):
    # Create list of reports (each input line is a report)
    # Each report is a list of numbers
    reports_list = []
    for report_in in input.split("\n"):
        num_list = [int(x) for x in report_in.split(" ")]
        reports_list.append(num_list)

    safe_count = 0
    for r in reports_list:
        if is_safe(r, dampener_val):
            safe_count += 1
    return safe_count


def is_safe(report, dampener_val=0):
    lev_1 = None
    inc = None
    failure = False

    for i, lev_2 in enumerate(report):
        # Initial case - initialize the value we're comparing against.  Nothing yet to compare, so continue into the loop
        if i == 0:
            lev_1 = lev_2
            continue

        # Compare this level with the prior one
        diff = lev_2 - lev_1

        # If the level has changed too much, automatically fail
        if abs(diff) < 1 or abs(diff) > 3:
            failure = True

        # If we're still checking conditions, check whether the value is increasing or decreasing
        if not failure:
            # If necessary, initialize inc boolean value
            if inc is None:
                inc = diff > 0

            # If we aren't following the prior pattern, fail
            if (inc and diff < 0) or (not inc and diff > 0):
                failure = True

        # In the case of failure, see if there's any tolerance remaining
        if failure:
            if dampener_val > 0:
                print(f"\nUsing dampener on report {report}")
                dampener_val -= 1
                failure = False

                # Special case if this is the 2nd element (for duplicate value) or 3rd (if changing inc/dec), since the report might be fixed with the first element resolved.
                if i <= 2:
                    if is_safe(report[1:], dampener_val):
                        return True
                
                # General case - remove the level that we're at and try again with decreased dampener
                # Note: Don't advance lev_1 if we're going to skip lev_2

                print(f"Removed: {lev_2}")
                # Test again with this value removed
                new_report = report[:i - 1] + report[i:]
                if is_safe(new_report, dampener_val):
                    return True

                continue
            print(f"{report}, false")
            return False

        # Increment the lev_1 counter for the next set of comparisons
        # Note, only if we didn't find a failure at this pass
        lev_1 = lev_2

    # The report has met the safety conditions for all levels
    return True


########### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###########
import lib

# Part 1, dampener = 0
# Part 2, dampener = 1
dampener_val = 1
use_example = False

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example)

    answer = process_input(input_text, dampener_val)
    print(answer)
