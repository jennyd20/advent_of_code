import lib


def find_lengths(space_image):
    print_image(space_image)
    expanded_img = expand_space(space_image)
    galaxies = find_galaxies(expanded_img)

    # Now find the lengths between all galaxy pairs
    print_image(expanded_img)
    sum_shortest_paths = 0
    while galaxies:
        from_gal = galaxies.pop()
        for to_gal in galaxies:
            xdif = abs(from_gal[0] - to_gal[0])
            ydif = abs(from_gal[1] - to_gal[1])
            # print(f"compare {from_gal[2]} to {to_gal[2]}")
            # print(f"xdif: {xdif}, ydif: {ydif}")
            # print(f"total diff: {xdif + ydif}")
            # print()
            sum_shortest_paths += xdif + ydif

    return sum_shortest_paths


def expand_space(original_space):
    # For part 1, we're only expanding x2
    expansion_value = 5
    if part1:
        expansion_value = 2
    print(f"{expansion_value=}")

    # Check every row and column at the same time
    expanded_space = []
    # Create a list of all columns, then eliminate cols that have galaxies in them.
    # At the end of the loop, all that's remaining will be the indices of empty columns
    empty_cols = [i for i in range(len(original_space[0]))]
    # Making the assumption that space is square

    for x, row in enumerate(original_space):
        expanded_space.append(row)
        # First, just check the whole line to see if the row is empty.
        # If so, add an extra empty row
        if row.find("#") < 0:
            for i in range(expansion_value - 1):
                expanded_space.append("." * len(row))
        for y in range(len(row)):
            if row[y] == "#":
                if y in empty_cols:
                    empty_cols.remove(y)

    # Now that we have tracked the empty columns, add them to every line in the list
    for x, row in enumerate(expanded_space):
        # Go through the list backwards to adding to empty columns so the addition doesn't mess up the stuff behind
        for col_to_add in reversed(empty_cols):
            row = row[:col_to_add] + "." * (expansion_value - 1) + row[col_to_add:]
        expanded_space[x] = row
    return expanded_space


def find_galaxies(image):
    # return {(x1, y1), (x2, y2), ... }
    galaxies = []
    for x, row in enumerate(image):
        for y in range(len(row)):
            if row[y] == "#":
                # Start counting from 1 instead of 0 to match example labeling of galaxies
                galaxy_num = len(galaxies) + 1

                # Messes things up for going through columns, but good for debugging
                # replaced_row_galaxy = row[:y] + str(galaxy_num) + row[y + 1 :]
                # image[x] = replaced_row_galaxy
                # row = replaced_row_galaxy
                galaxies.append([x, y, galaxy_num])
    print(f"Number of galaxies: {len(galaxies)}")
    return galaxies


def print_image(image):
    for i in image:
        print(i)
    print()


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = True
part1 = False
alt_file = None
# alt_file = "day11_ex2.txt"

# Execute the scriptl
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_file)
    answer = find_lengths(input_text.splitlines())
    print(answer)

"""
For part 2:

Trying to run programmatically will cause the CPU to explode

Expanding empty space x1,000,000 instead of x2

number of pairings = n*(n+1) / 2

In example:
9 total galaxies
36 pairs

x1 = 292
x2 = 374
x3 = 456
x4 = 538
x5 = 620
x10 = 1030 
x100 = 8410


My input:
443 galaxies
98346 pairs

"""
