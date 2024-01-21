import lib


def get_beam_load(platform):
    # For part 1, roll the rocks north once then calculate the load.
    if not part2:
        platform = rotate_and_tilt(platform)
        # For part 1, we need to rotate the platform back before calculating the load
        rotated_platform = untilt(platform)
        return calculate_load(rotated_platform)

    # Else, part 2 shenanigans!
    # A full cycle is rolling boulders 4 times (north, west, south, east)
    # Four rotations puts the platform back in its original orientation, so don't need to do any tilting here
    # Track where we are at the end of a cycle so if we've hit that state before we know we've completed a full period
    seen_states = {}

    num_cycles = 1000000000
    i = 0
    skip_ahead = False
    skipped = False

    while i < num_cycles:
        # Roll the rocks in all four directions - rolling will reset the orientation at the end of the cycle
        for _ in range(4):
            platform = rotate_and_tilt(platform)

        platform_key = tuple(platform)
        if platform_key in seen_states.keys():
            skip_ahead = True
        else:
            seen_states[platform_key] = i

        # Found a repeat - calculate the period and advance to the end of the cycle count within that period
        if skip_ahead and not skipped:
            start_idx = seen_states.get(platform_key)
            end_idx = i
            period = end_idx - start_idx
            num_skipped = (num_cycles - i) // period - 1
            i += period * num_skipped
            skipped = True
        i += 1

    return calculate_load(platform)


# Turn columns into row-strings to move rocks.
# The new platform will be rotated 90 from the original
# The original platform's columns are the new platform's rows
def rotate_and_tilt(platform):
    new_platform = []

    height = len(platform)
    width = len(platform[0])

    for i in range(width):
        # Generate each column of the platform and turn it into a string
        col = ""
        for j in range(height):
            col += platform[height - j - 1][i]

        tipped_col = ""
        rocks_in_group = 0
        ground_in_group = 0

        # For each column (now a horizontal string), find the rolled version
        # Add it to the new platform object, which will be rotated 90 degrees from the input
        for x in col:
            if x == "O":
                rocks_in_group += 1
            elif x == ".":
                ground_in_group += 1
            else:  # x == "#"
                # Collect rocks into a group
                tipped_col += "." * ground_in_group
                tipped_col += "O" * rocks_in_group
                tipped_col += "#"
                rocks_in_group = 0
                ground_in_group = 0
        else:
            # When we reach the end of the column, make sure to add any extra rolled rocks
            tipped_col += "." * ground_in_group
            tipped_col += "O" * rocks_in_group

        new_platform.append(tipped_col)
    return new_platform


# Only used for part 1, so that the load calculations are the same between part 1 and part 2
def untilt(platform):
    height = len(platform)
    width = len(platform[0])
    rotated_platform = []
    for i in range(width):
        row_from_col = ""
        for j in range(height):
            c = platform[j][width - i - 1]
            row_from_col += c
        rotated_platform.append(row_from_col)
    return rotated_platform


def calculate_load(platform):
    height = len(platform)
    load = 0
    for idx, line in enumerate(platform):
        for c in line:
            if c == "O":
                load += height - idx
    return load


def print_platform(platform):
    print("\n".join(platform))
    print()


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = True
new_file = None  # "day14_ex2.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, new_file)
    answer = get_beam_load(input_text.splitlines())
    print(answer)
