import lib


def print_record_at_index(record, enums, idx, in_group):
    print(f"{enums=}; {in_group=}")
    print(record)
    print((" " * max(0, idx - 1)) + ("^") + (" " * (len(record) - idx)) + "\n")


def get_num_options(record, enums, idx=0, in_group=False):
    print_record_at_index(record, enums, idx, in_group)

    # Return case - we're at the end of the record line
    if idx == len(record):
        if len(enums) == 0 or (len(enums) == 1 and enums[0] == 0):
            # No more enumerations, or one last enumeration that only contains 0 - valid case
            return 1
        else:
            # If there are still enumerations remaining or the last enumeration isn't zero, this isn't a valid case
            return 0

    # We haven't made it to the end of the string yet, do more work
    # If the enum we're checking is equal to 0
    # if enums and enums[0] == 0:  # was before
    if not enums or (enums and enums[0] == 0):  # girts
        match record[idx]:
            # Not expecting more and found one, invalid case
            case "#":
                return 0
            # "." or "?" will end this group, because the ? has to be a dot.  Continue to the next group.
            case _:
                mod_record = record[:idx] + "." + record[idx + 1 :]
                # Go to the next enum if there is one, otherwise recurse again to make sure that we've finished processing the record
                new_enum = enums[1:] if enums else []  # girts: the "if enums" here is extra, since "if" above guarantees that
                return get_num_options(mod_record, new_enum, idx + 1, False)

    # All other cases where the enum > 0
    
    match record[idx]:
        case ".":
            # If a period and we're already in a group, prune this invalid branch
            if in_group:
                return 0
            # If we aren't in a group now, we're still looking for the next group.  Advance index and keep checking.
            else:
                return get_num_options(record, enums, idx + 1, False)
        case "#":
            # In a group; valid so far, so keep going down this path with a decremented enumeration
            # If there aren't any more enumerations to do, pass an empty list
            return get_num_options(record, decrement_enum(enums), idx + 1, True)
        case "?":
            # If we're already in a group, the valid thing for the "?" to be is a "#".  Advance accordingly.
            if in_group:
                new_enums = []
                if enums:  # girts: can this ever be False? we can't have in_group=True but empty enums, right?
                    new_enums = enums[:]
                    new_enums[0] -= 1
                mod_record = record[:idx] + "#" + record[idx + 1 :]
                return get_num_options(record, new_enums, idx + 1, True)  # girts: should "record" be "mod_record"?
            else:
                # Not currently in a group.  Test both in-a-group case and not-in-a-group case and return the sum.
                record_group = record[:idx] + "#" + record[idx + 1 :]
                record_no_group = record[:idx] + "." + record[idx + 1 :]
                sum = get_num_options(
                    record_no_group, enums, idx + 1, False
                )
                if enums:
                    sum += get_num_options(record_group, decrement_enum(enums), idx + 1, True)
                return sum

    raise ValueError("Something has went horribly wrong and no cases have been matched")


def decrement_enum(enums):
    if not enums:  # girts
        pass
    new_enums = []
    if enums:
        new_enums = enums[:]
        new_enums[0] -= 1
    return new_enums


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False # True
part1 = True
custom = None # "day12_tests.txt"

# Execute the scriptl
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, custom)

    answer = 0
    for row in input_text.splitlines():
        record, enums = row.split(" ")
        enums = [int(x) for x in enums.split(",")]
        num_arrangements = get_num_options(record, enums)
        print(f"{num_arrangements=} for {record=} with {enums=}")
        answer += num_arrangements

    print(answer)


'''
num_arrangements=1 for record='#.?????#.#????#' with enums=[1, 4, 6]
num_arrangements=1 for record='..#?#??#?????#??' with enums=[4, 9]
'''