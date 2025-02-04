from aoc_libs import grid as grid_lib


def process_input(input, part1):
    map = grid_lib.Grid.create_from_input(input)
    # map.print()
    # print()

    # Figure out where all the
    ant_positions = map.to_dict()

    # Don't care about the blank spaces, just the antenna spaces
    del ant_positions["."]

    all_antinode_pos = set()
    for ant in ant_positions:
        all_antinode_pos.update(calculate_antinodes(map, ant_positions[ant], part1))

    # Prettify the result for debugging purposes
    # map.set_all_val_pos("*", all_antinode_pos)
    # map.print()

    return len(all_antinode_pos)


def calculate_antinodes(
    map: grid_lib.Grid, pos: set[grid_lib.Position], part1: bool
) -> set[grid_lib.Position]:
    antinodes = set()
    for p1 in pos:
        for p2 in pos:
            if p1 == p2:
                continue

            # For all potential pairs in a frequency, calculate the antipodes for that pair
            row_diff = p2.row - p1.row
            col_diff = p2.col - p1.col

            # Find the antinode(s) on both sides of the pair
            # print(f"\nAdding antinodes for {p1=}, {p2=}\t{row_diff=}, {col_diff=}")

            antinodes.update(
                get_antinodes_from_point(map, p1, -row_diff, -col_diff, part1)
            )
            antinodes.update(
                get_antinodes_from_point(map, p2, row_diff, col_diff, part1)
            )
            
            # Make sure to add the locations of the original pair
            if not part1:
                antinodes.update({p1, p2})

    return antinodes


def get_antinodes_from_point(map, start_pos, row_diff, col_diff, part1):
    print(f"- Starting at point {start_pos}\t\t\t{row_diff=}, {col_diff=}")
    antinodes = set()

    # In part 2, each antenna is also an antinode since
    # they are part of the line demarcated by two antenna
    if not part1:
        antinodes.add(start_pos)

    # Get the position past a particual pair's point.
    antinode = grid_lib.Position(start_pos.row + row_diff, start_pos.col + col_diff)
    while antinode.in_bounds(map):
        antinodes.add(antinode)
        # print(f"  - added antinode at {antinode}")
        antinode = grid_lib.Position(antinode.row + row_diff, antinode.col + col_diff)
        if part1:
            # For part 1 - break at just the first antipode.
            # For part 2 - keep looking until the edge of the map.
            break

    return antinodes


########### SCRIPT ARGUMENTS AND EXECUTION ###########
from aoc_libs import lib


def main(part1=True, use_example=False):
    print(f"{part1=}, {use_example=}")
    input_text = lib.read_input(__file__, use_example)
    return process_input(input_text, part1)


if __name__ == "__main__":
    print(main(part1=False, use_example=False))
