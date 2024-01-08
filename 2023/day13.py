import lib


def process_mirror(mirror):
    mirror = mirror.splitlines()
    reflected_num = 0

    # Check both the horizontal and vertical map cases
    for is_horizontal in {True, False}:
        # The problem guarantees a single line of reflection in a given mirror
        reflected_num = find_reflection_pos(mirror, is_horizontal)
        if reflected_num:
            return reflected_num

    raise ValueError(f"**** No reflections in this mirror: {mirror=} ****")


def find_reflection_pos(mirror, is_horizontal):
    # For a horizontal reflection, transpose the table so that we can use the same algorithm on rows
    mirror = transpose_mirror(mirror) if is_horizontal else mirror

    # Get the available mirror options for a particular mirror
    mirror_options = get_mirror_options(mirror)

    # In part 1, if there is no reflection in this direction then we're done
    if not part2 and not mirror_options:
        return 0

    # In part 2, even if we didn't find a reflection the first time we can re-run the map with smudges
    if part2:
        # If present, get the original reflection of this map to remove it from future reflection options
        # (as per part 2 spec)
        orig_reflection = mirror_options.pop() if mirror_options else -1
        mirror_options = get_smudged_mirror_options(mirror, orig_reflection)

    return get_mirror_value(mirror_options, is_horizontal)


def get_mirror_options(mirror):
    mirror_options = None

    for row in mirror:
        row_options = get_row_options(row)
        # For the first row, compare everything against that set
        if not mirror_options:
            mirror_options = row_options
        # For all other rows, find the intersection or prior sets with the current set
        else:
            mirror_options = mirror_options.intersection(row_options)
            if not mirror_options:
                # Shortcut if there's a row that matches no other rows, meaning there will be no mirrored line
                return None
    return mirror_options


def get_smudged_mirror_options(mirror, orig_reflection=-1):
    for x, row in enumerate(mirror):
        smudged_mirror = mirror.copy()
        smudged_mirror_options = None
        for y, c in enumerate(row):
            smudged_row = row[:y] + get_opposite(c) + row[y + 1 :]
            smudged_mirror[x] = smudged_row
            smudged_mirror_options = get_mirror_options(smudged_mirror)
            if not smudged_mirror_options:
                continue
            if orig_reflection in smudged_mirror_options:
                smudged_mirror_options.remove(orig_reflection)
            if smudged_mirror_options:
                return smudged_mirror_options
    return None


def get_row_options(row):
    # Check each possible location in this particular row for a reflection
    row_options = set()
    for mirror_idx in range(len(row) - 1):
        if is_mirror(row, mirror_idx):
            row_options.add(mirror_idx)
    return row_options


def get_opposite(x):
    return "#" if x == "." else "."


def is_mirror(row, mirror_idx):
    # Check from this index to the end of the line
    # The reflection go to either the far left or the far right, so find the smaller value to traverse
    # The columns not checked will be outside the reflective range
    mirror_width = min(mirror_idx + 1, len(row) - mirror_idx - 1)
    for i in range(mirror_width):
        if row[mirror_idx - i] != row[mirror_idx + i + 1]:
            return False
    return True


def get_mirror_value(options, is_horizontal):
    if not options:
        return 0
    # There should only be one value at this point.
    assert len(options) == 1
    # The recorded index is one below the reflection, so add one
    value = options.pop() + 1
    # As per spec, vertical is *1 and horizontal is *100
    return value * (100 if is_horizontal else 1)


def transpose_mirror(mirror):
    new_mirror = []
    for col in range(len(mirror[0])):
        new_row = ""
        for row in mirror:
            new_row += row[col]
        new_mirror.append(new_row)
    return new_mirror


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part2 = True
file = None
# file = "day13_ex3.txt"

# Execute the script
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, file)
    answer = sum(process_mirror(mirror) for mirror in input_text.split("\n\n"))
    print(answer)
