import lib


def find_lengths(space_image):
    empty_rows_and_cols, galaxy_list = process_space(space_image)

    # Now find the lengths between all galaxy pairs
    if part1:
        expansion_multiplier = 2
    else:
        expansion_multiplier = 1000000

    sum_shortest_paths = 0

    while galaxy_list:
        from_gal = galaxy_list.pop()
        for to_gal in galaxy_list:
            # Determine how many empty rows/cols are crossed between the paths
            # index 1 is row, index 2 is col.  Check both instead of duplicating code
            total_expansions = 0
            axis_diff = 0
            for i in range(2):
                from_gal_i = from_gal[i]
                to_gal_i = to_gal[i]
                axis_diff += abs(from_gal_i - to_gal_i)
                for x in empty_rows_and_cols[i]:
                    if min(from_gal_i, to_gal_i) < x < max(from_gal_i, to_gal_i):
                        total_expansions += 1

            sum_shortest_paths += (
                axis_diff + (total_expansions * (expansion_multiplier - 1))
            )

    return sum_shortest_paths


def process_space(original_space):
    # Just return a list of rows and a list of columns that are empty and will be expanded

    empty_rows = set()

    # Create a list of all columns, then eliminate cols that have galaxies in them.
    # At the end of the loop, all that's remaining will be the indices of empty columns
    # Making the assumption that space is square
    empty_cols = set(range(len(original_space[0])))

    galaxy_list = []

    for x, row in enumerate(original_space):
        row_is_empty = True
        for y, point in enumerate(row):
            if row[y] == "#":
                galaxy_list.append([x, y])
                row_is_empty = False
                if y in empty_cols:
                    empty_cols.remove(y)
        if row_is_empty:
            empty_rows.add(x)

    return [empty_rows, empty_cols], galaxy_list


### SCRIPT ARGUMENTS AND GLOBAL VARIABLES ###
use_example = False
part1 = False
alt_file = None
# alt_file = "day11_ex2.txt"

# Execute the scriptl
if __name__ == "__main__":
    input_text = lib.read_input(__file__, use_example, alt_file)
    answer = find_lengths(input_text.splitlines())
    print(answer)
